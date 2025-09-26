# Data Flows & Processing Pipelines

This document details the various data flows within the Sushi Kitchen architecture, from user interactions to deployed configurations.

## Primary Data Flows

### 1. User Request to Generated Compose

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant API
    participant Orchestrator
    participant CoreScripts
    participant FileSystem

    User->>WebUI: Select platter/combo
    WebUI->>API: POST /api/v1/compose/generate
    API->>Orchestrator: generate_complete_stack()

    Orchestrator->>CoreScripts: execute generate-compose.py
    CoreScripts->>FileSystem: read manifests
    FileSystem-->>CoreScripts: return manifest data
    CoreScripts-->>Orchestrator: return base compose YAML

    Orchestrator->>CoreScripts: execute generate-network-config.py
    CoreScripts-->>Orchestrator: return networked compose

    Orchestrator->>Orchestrator: apply_security_policies()
    Orchestrator-->>API: return final compose dict

    API->>API: validate configuration
    API-->>WebUI: return GenerateResponse
    WebUI-->>User: display compose + download option
```

### 2. CI/CD Bundle Generation

```mermaid
flowchart TD
    A[Git Push to main] --> B[GitHub Actions Trigger]
    B --> C[Install Dependencies]
    C --> D[Verify Manifest Structure]
    D --> E[Generate API Bundle]
    E --> F[Generate TypeScript Types]
    F --> G[Validate Generated Files]
    G --> H[Create Version Tag]
    H --> I[Upload Artifacts]
    I --> J[Deploy to S3]
    J --> K[Invalidate API Cache]
    K --> L[Update PR Comments]

    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style J fill:#e8f5e8
```

### 3. Component Discovery Flow

```mermaid
flowchart LR
    subgraph "API Request"
        A[GET /api/v1/components]
    end

    subgraph "Cache Layer"
        B{Bundle Exists?}
        C[Load from generated/api-bundle.json]
        D[Dynamic Generation via Scripts]
    end

    subgraph "Response Processing"
        E[Transform to API Format]
        F[Return ComponentsResponse]
    end

    A --> B
    B -->|Yes| C
    B -->|No| D
    C --> E
    D --> E
    E --> F
```

## Data Transformation Pipeline

### Manifest Processing

```mermaid
flowchart TD
    subgraph "Input Sources"
        A[contracts.yml]
        B[combos.yml]
        C[platters.yml]
        D[network-profiles.yml]
    end

    subgraph "Processing Steps"
        E[YAML Parser]
        F[Dependency Resolver]
        G[Capability Matcher]
        H[Conflict Detector]
    end

    subgraph "Intermediate Data"
        I[Resolved Service Graph]
        J[Network Assignments]
        K[Security Policies]
    end

    subgraph "Output Formats"
        L[Docker Compose YAML]
        M[API Bundle JSON]
        N[TypeScript Definitions]
    end

    A --> E
    B --> E
    C --> E
    D --> E

    E --> F
    F --> G
    G --> H

    H --> I
    I --> J
    J --> K

    K --> L
    K --> M
    K --> N
```

### Service Resolution Logic

```python
# Pseudocode for service resolution
def resolve_services(selection_id: str, selection_type: str) -> Set[str]:
    initial_services = get_services_for_selection(selection_id, selection_type)
    resolved_services = set()

    for service in initial_services:
        resolved_services.add(service)

        # Resolve required capabilities
        for capability in service.requires:
            provider = find_capability_provider(capability)
            if provider:
                resolved_services.add(provider)

        # Add suggested services
        for suggestion in service.suggests:
            if suggestion not in conflicts:
                resolved_services.add(suggestion)

    return resolved_services
```

## Network Security Data Flow

### Profile Application Process

```mermaid
flowchart TD
    A[Base Docker Compose] --> B[Select Network Profile]
    B --> C{Profile Type}

    C -->|chirashi| D[Single Bridge Network]
    C -->|temaki| E[3-Tier Segmentation]
    C -->|inari| F[Multi-Tier Isolation]

    D --> G[Assign All Services to sushi_net]
    E --> H[Classify Services by Function]
    F --> I[Apply Strict Network Policies]

    H --> J[Web → Frontend Network]
    H --> K[App → Backend Network]
    H --> L[Data → Data Network]

    I --> M[Web → Web Tier]
    I --> N[App → App Tier]
    I --> O[Data → Data Tier]
    I --> P[Monitoring → Mgmt Tier]

    G --> Q[Apply Basic Security]
    J --> R[Apply Business Security]
    K --> R
    L --> R
    M --> S[Apply Enterprise Security]
    N --> S
    O --> S
    P --> S

    Q --> T[Final Compose Configuration]
    R --> T
    S --> T
```

### Service Classification Logic

```python
def classify_service(service_name: str, service_config: Dict) -> str:
    """Determine network tier for a service based on its characteristics"""

    # Web-facing services
    if service_name in ['caddy', 'homepage', 'grafana', 'n8n']:
        return 'web'

    # Check for exposed HTTP ports
    ports = service_config.get('ports', [])
    if any('80' in str(port) or '443' in str(port) for port in ports):
        return 'web'

    # Data services
    if service_name in ['postgres', 'neo4j', 'redis', 'qdrant']:
        return 'data'

    # Management/monitoring
    if service_name in ['prometheus', 'grafana', 'cadvisor']:
        return 'management'

    # Default to application tier
    return 'application'
```

## API Data Structures

### Request/Response Flow

```mermaid
flowchart TD
    subgraph "Client Request"
        A[GenerateRequest]
        A1[selection_type: string]
        A2[selection_id: string]
        A3[privacy_profile: string]
        A4[include_optional: boolean]
    end

    subgraph "Server Processing"
        B[Validation Layer]
        C[Orchestration Layer]
        D[Generation Layer]
        E[Security Layer]
    end

    subgraph "Server Response"
        F[GenerateResponse]
        F1[yaml: string]
        F2[services: string[]]
        F3[profile: string]
        F4[success: boolean]
        F5[validation: ValidationResult]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

    A -.-> A1
    A -.-> A2
    A -.-> A3
    A -.-> A4

    F -.-> F1
    F -.-> F2
    F -.-> F3
    F -.-> F4
    F -.-> F5
```

### Bundle Structure

```json
{
  "version": "1.0.0",
  "generated_at": "2024-01-15T10:30:00Z",
  "build": {
    "version_tag": "bundle-20240115-103000-a1b2c3d4",
    "commit_sha": "a1b2c3d4e5f6...",
    "branch": "main",
    "workflow_run": "12345"
  },
  "checksums": {
    "contracts.yml": "sha256:abc123...",
    "combos.yml": "sha256:def456...",
    "platters.yml": "sha256:789xyz..."
  },
  "services": {
    "hosomaki.redis": {
      "id": "hosomaki.redis",
      "name": "Redis Cache",
      "category": "hosomaki",
      "provides": ["cap.cache"],
      "requires": ["cap.networking"],
      "docker": {...},
      "resource_requirements": {...}
    }
  },
  "combos": {...},
  "platters": {...},
  "capabilities": {...},
  "network_profiles": {...}
}
```

## Error Handling & Validation

### Validation Pipeline

```mermaid
flowchart TD
    A[Generated Configuration] --> B[Syntax Validation]
    B --> C[Dependency Validation]
    C --> D[Network Validation]
    D --> E[Security Validation]
    E --> F[Resource Validation]

    B -->|Invalid YAML| G[Syntax Error]
    C -->|Missing Dependencies| H[Dependency Error]
    D -->|Network Conflicts| I[Network Error]
    E -->|Security Violations| J[Security Error]
    F -->|Resource Issues| K[Resource Warning]

    F -->|All Valid| L[Success Response]

    G --> M[Error Response]
    H --> M
    I --> M
    J --> M
    K --> N[Warning Response]
```

### Error Response Structure

```typescript
interface ValidationResult {
  valid: boolean;
  warnings: string[];
  errors: string[];
}

interface ErrorResponse {
  success: false;
  error: string;
  details?: ValidationResult;
  timestamp: string;
}
```

## Performance Optimization

### Caching Strategy

```mermaid
flowchart TD
    subgraph "Cache Layers"
        A[In-Memory Component Cache]
        B[Generated Bundle Cache]
        C[Compiled Template Cache]
    end

    subgraph "Cache Invalidation"
        D[Git Webhook]
        E[Manual Admin Endpoint]
        F[TTL Expiration]
    end

    subgraph "Cache Warming"
        G[CI/CD Bundle Generation]
        H[Background Pre-compilation]
        I[Startup Cache Loading]
    end

    A --> B --> C
    D --> A
    E --> B
    F --> C
    G --> B
    H --> C
    I --> A
```

### Data Loading Optimization

```python
class OptimizedDataLoader:
    def __init__(self):
        self._bundle_cache = {}
        self._last_modified = {}

    async def load_bundle(self) -> Dict:
        bundle_path = self.generated_dir / 'api-bundle.json'

        # Check if file has been modified
        current_mtime = bundle_path.stat().st_mtime
        cached_mtime = self._last_modified.get('bundle')

        if cached_mtime and current_mtime <= cached_mtime:
            return self._bundle_cache['bundle']

        # Load and cache new data
        with bundle_path.open() as f:
            bundle = json.load(f)

        self._bundle_cache['bundle'] = bundle
        self._last_modified['bundle'] = current_mtime

        return bundle
```

## Monitoring & Observability

### Data Flow Metrics

```mermaid
flowchart LR
    subgraph "Request Metrics"
        A[Request Count]
        B[Response Time]
        C[Error Rate]
        D[Validation Failures]
    end

    subgraph "Generation Metrics"
        E[Script Execution Time]
        F[Bundle Size]
        G[Service Count]
        H[Network Complexity]
    end

    subgraph "System Metrics"
        I[Memory Usage]
        J[CPU Usage]
        K[Disk I/O]
        L[Network I/O]
    end

    A --> M[Prometheus]
    B --> M
    C --> M
    D --> M
    E --> M
    F --> M
    G --> M
    H --> M
    I --> M
    J --> M
    K --> M
    L --> M

    M --> N[Grafana Dashboard]
```

### Health Check Data Flow

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check covering all data flows"""

    checks = {
        "core_repo_accessible": check_core_repo(),
        "scripts_available": check_scripts(),
        "bundle_cache_healthy": check_bundle_cache(),
        "generation_pipeline": check_generation(),
        "network_profiles": check_network_profiles(),
        "typescript_types": check_types()
    }

    overall_health = all(checks.values())

    return {
        "status": "healthy" if overall_health else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "version": get_version_info()
    }
```

This data flow documentation provides the technical details needed to understand how data moves through the Sushi Kitchen architecture, from user interactions to deployed configurations.