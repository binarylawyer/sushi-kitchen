# 🍣 Enterprise RAG Deployment Example

*How the same document question-answering system transforms when enterprise security, monitoring, and compliance requirements are applied*

## Executive Summary

**Scenario**: A mid-size company wants to deploy the same document chat functionality from our basic example, but with enterprise-grade security, monitoring, backup systems, and user access controls appropriate for business use.

**Key Differences from Basic Setup**:
- **Security**: Single sign-on (SSO), network segmentation, audit logging
- **Monitoring**: Comprehensive system monitoring, alerting, performance tracking  
- **Backup**: Automated backups with encryption and retention policies
- **Access Control**: Role-based permissions, user management, session controls
- **Compliance**: Audit trails, data retention policies, security reporting

**Target Users**: IT administrators, platform engineers, security teams

## Business Requirements

### Functional Requirements
1. **Document Processing**: Same core functionality as basic setup - upload documents and ask questions
2. **User Management**: Multiple users with different access levels (admin, editor, viewer)
3. **Single Sign-On**: Integration with company Active Directory or LDAP
4. **Audit Logging**: Complete audit trail of user actions and system events
5. **Data Backup**: Automated daily backups with 90-day retention
6. **System Monitoring**: Real-time monitoring with alerts for system issues

### Non-Functional Requirements
1. **Security**: Network isolation, encrypted communications, secure authentication
2. **Availability**: 99.5% uptime during business hours (8am-6pm)
3. **Performance**: Support 50 concurrent users, <3 second response times
4. **Scalability**: Ability to scale to 200 users and 10,000 documents
5. **Compliance**: Audit-ready logging and reporting for security reviews

## Architecture Evolution

### From Basic to Enterprise

The manifest system transforms the basic setup by automatically adding enterprise capabilities:

#### Core Services (Enhanced)
- **Ollama**: Same LLM inference but with production settings and monitoring
- **AnythingLLM**: Enhanced with SSO integration and audit logging
- **Qdrant**: Production configuration with backup and monitoring
- **PostgreSQL**: Enterprise setup with replication and backup

#### Added Enterprise Services
- **Authentik**: SSO identity provider with LDAP integration
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Dashboards and alerting
- **Caddy**: Reverse proxy with SSL termination and security headers
- **Backup Service**: Automated backup with encryption

#### Enhanced Configuration
- **Network Profile**: `business_confidential` with network segmentation
- **Environment**: `production` with optimized performance and security
- **Security**: Comprehensive access controls and audit logging

## Manifest System Processing

### Service Selection Evolution

Starting from the basic combo, enterprise requirements drive additional service selection:

```yaml
# Original selection
base_combo: combo.chat-local
includes: [hosomaki.ollama, hosomaki.anythingllm]

# Enterprise enhancement selection  
additional_services:
  - gunkanmaki.authentik    # SSO and user management
  - inari.prometheus        # Metrics collection
  - inari.grafana          # Monitoring dashboards
  - hosomaki.caddy         # Reverse proxy and SSL
  
# Automatic additions for enterprise requirements
auto_added_services:
  - futomaki.qdrant        # Vector storage (same as basic)
  - futomaki.postgresql    # Relational storage (enhanced config)
  - futomaki.redis         # Session storage for SSO
```

### Configuration Transformations

The manifest system applies enterprise-grade configurations:

#### Network Segmentation (business_confidential profile)
```yaml
# Frontend Network: User-facing services
frontend_tier:
  - hosomaki.caddy         # Reverse proxy
  - gunkanmaki.authentik   # Authentication portal

# Backend Network: Processing services  
backend_tier:
  - hosomaki.anythingllm   # Document chat interface
  - hosomaki.ollama        # LLM inference
  - inari.prometheus       # Metrics collection

# Data Network: Storage services
data_tier:
  - futomaki.postgresql    # Application database
  - futomaki.qdrant        # Vector database
  - futomaki.redis         # Session cache
```

#### Security Enhancements
```yaml
# Authentication and authorization
auth_config:
  sso_provider: authentik
  session_timeout: 8_hours
  mfa_required: true
  password_policy: enterprise

# Network security
network_security:
  tls_everywhere: true
  security_headers: enabled
  rate_limiting: enabled
  firewall_rules: restrictive

# Audit logging
audit_config:
  log_all_access: true
  log_retention: 90_days
  log_encryption: true
  compliance_reports: weekly
```

#### Monitoring and Alerting
```yaml
# Monitoring stack
monitoring_config:
  metrics_retention: 30_days
  alerting_enabled: true
  dashboard_access: role_based
  
# Alert thresholds
alerts:
  cpu_usage: 80%
  memory_usage: 85%
  disk_usage: 90%
  response_time: 3_seconds
  error_rate: 1%
```

## Generated Enterprise Architecture

### Complete Service Stack

The enterprise deployment includes 8 services working together:

```yaml
services:
  # Frontend Tier (sushi_frontend network)
  caddy:           # Reverse proxy, SSL termination, security headers
  authentik:       # SSO provider, user management, MFA
  
  # Backend Tier (sushi_backend + sushi_frontend networks)
  anythingllm:     # Document chat interface (enhanced with SSO)
  ollama:          # LLM inference (production configuration)
  prometheus:      # Metrics collection and monitoring
  
  # Data Tier (sushi_data network only)
  postgresql:      # Application database (with replication)
  qdrant:          # Vector database (with backup)
  redis:           # Session cache and queue storage
  
  # Monitoring Tier (access to all networks)
  grafana:         # Monitoring dashboards and alerting
```

### Network Architecture

```mermaid
graph TB
    subgraph "Frontend Network (sushi_frontend)"
        C[Caddy Proxy]
        A[Authentik SSO]
    end
    
    subgraph "Backend Network (sushi_backend)"
        AL[AnythingLLM]
        O[Ollama]
        P[Prometheus]
    end
    
    subgraph "Data Network (sushi_data)"
        PG[PostgreSQL]
        Q[Qdrant]
        R[Redis]
    end
    
    subgraph "Monitoring (crosses all networks)"
        G[Grafana]
    end
    
    Internet --> C
    C --> A
    C --> AL
    A --> AL
    AL --> O
    AL --> PG
    AL --> Q
    A --> R
    P --> G
    G --> Internet
```

### Data Flow and Security

#### User Authentication Flow
1. **User Access**: User navigates to company.com/docs
2. **Proxy**: Caddy receives request, enforces HTTPS and security headers
3. **Authentication**: Authentik checks for valid session
4. **SSO Integration**: If not authenticated, redirects to company LDAP/AD
5. **Authorization**: Authentik verifies user permissions for document access
6. **Application Access**: Authenticated user reaches AnythingLLM interface

#### Document Processing Flow
1. **Upload**: Authenticated user uploads document through AnythingLLM
2. **Processing**: AnythingLLM processes document using Ollama for embeddings
3. **Storage**: Document embeddings stored in Qdrant, metadata in PostgreSQL
4. **Audit**: All actions logged to audit trail with user identity
5. **Backup**: Nightly backup captures all document data with encryption

#### Query Processing Flow
1. **Question**: User asks question about documents
2. **Vector Search**: AnythingLLM queries Qdrant for relevant document chunks
3. **LLM Inference**: Ollama generates answer based on context
4. **Monitoring**: Prometheus captures performance metrics
5. **Audit**: Query and response logged for compliance

## Deployment Guide

### Prerequisites

#### Infrastructure Requirements
- **Compute**: 16 CPU cores, 32GB RAM minimum
- **Storage**: 200GB SSD with daily backup capability
- **Network**: Dedicated subnet with firewall controls
- **SSL**: Valid SSL certificate for company domain
- **Directory**: LDAP/Active Directory integration available

#### Security Requirements
- **Firewall**: Only ports 80, 443 exposed externally
- **Certificates**: Valid SSL certificates for all endpoints
- **Backup**: Encrypted backup storage with offsite replication
- **Monitoring**: Security team access to monitoring dashboards

### Configuration Steps

#### 1. Environment Setup
```bash
# Generate enterprise configuration
sushi-kitchen generate \
  --combo chat-local \
  --add-service gunkanmaki.authentik \
  --add-service inari.prometheus \
  --add-service inari.grafana \
  --add-service hosomaki.caddy \
  --profile business_confidential \
  --environment production

# Set enterprise environment variables
cp .env.enterprise .env
```

#### 2. Security Configuration
```bash
# Configure SSL certificates
export SSL_CERT_PATH="/path/to/company.crt"
export SSL_KEY_PATH="/path/to/company.key"

# Set secure passwords
export POSTGRES_PASSWORD="$(openssl rand -base64 32)"
export GRAFANA_ADMIN_PASSWORD="$(openssl rand -base64 32)"
export AUTHENTIK_SECRET_KEY="$(openssl rand -base64 50)"

# Configure LDAP integration
export LDAP_SERVER="ldaps://company.com:636"
export LDAP_BIND_DN="CN=sushi-service,OU=Service Accounts,DC=company,DC=com"
export LDAP_BIND_PASSWORD="${LDAP_SERVICE_PASSWORD}"
```

#### 3. Network Setup
```bash
# Create dedicated Docker networks for security
docker network create sushi_frontend --subnet 172.21.0.0/24
docker network create sushi_backend --subnet 172.22.0.0/24  
docker network create sushi_data --subnet 172.23.0.0/24
```

#### 4. Storage and Backup
```bash
# Create encrypted volumes
docker volume create sushi_postgresql_data
docker volume create sushi_qdrant_data
docker volume create sushi_backup_storage

# Configure backup encryption
export BACKUP_ENCRYPTION_KEY="$(openssl rand -base64 32)"
```

#### 5. Deploy Services
```bash
# Start infrastructure services first
docker-compose up -d postgresql redis qdrant

# Wait for databases to be ready
docker-compose exec postgresql pg_isready
docker-compose exec redis redis-cli ping
docker-compose exec qdrant curl -f http://localhost:6333/health

# Start application services
docker-compose up -d ollama authentik caddy

# Start monitoring stack
docker-compose up -d prometheus grafana

# Finally start user-facing application
docker-compose up -d anythingllm
```

### Initial Configuration

#### 1. Authentik SSO Setup
```bash
# Access Authentik admin interface
open https://auth.company.com/if/admin/

# Configure LDAP provider
# - Server: ldaps://company.com:636
# - Bind DN: Service account credentials
# - User DN: OU=Users,DC=company,DC=com
# - Group DN: OU=Groups,DC=company,DC=com

# Create application for AnythingLLM
# - Name: Document Chat System
# - Provider: OIDC
# - Client ID: anythingllm
# - Redirect URI: https://docs.company.com/auth/oidc/callback
```

#### 2. AnythingLLM Integration
```bash
# Configure OIDC in AnythingLLM
# - Provider: Custom OIDC
# - Discovery URL: https://auth.company.com/application/o/anythingllm/.well-known/openid_configuration
# - Client ID: anythingllm
# - Client Secret: ${OIDC_CLIENT_SECRET}
```

#### 3. Monitoring Setup
```bash
# Import Grafana dashboards
curl -X POST https://admin:${GRAFANA_ADMIN_PASSWORD}@monitoring.company.com/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @grafana-dashboards/sushi-kitchen-overview.json

# Configure Prometheus alerts
docker-compose exec prometheus promtool check rules /etc/prometheus/alerts/*.yml
```

## Monitoring and Management

### System Dashboards

#### 1. Executive Dashboard
- **System Health**: Overall status of all services
- **User Activity**: Active sessions, document uploads, queries per hour
- **Performance**: Average response times, system resource utilization
- **Security**: Failed login attempts, security alerts, audit summary

#### 2. Operations Dashboard  
- **Infrastructure**: CPU, memory, disk, network utilization per service
- **Application**: Request rates, error rates, response times
- **Database**: Query performance, connection pools, transaction rates
- **Storage**: Document counts, vector database performance

#### 3. Security Dashboard
- **Authentication**: Login success/failure rates, MFA usage
- **Network**: Traffic patterns, blocked requests, security events
- **Audit**: Data access patterns, privilege escalations, compliance metrics
- **Alerts**: Active security alerts, incident response status

### Alerting Strategy

#### Critical Alerts (Immediate Response)
- Service downtime (any core service unavailable)
- Database connection failures
- Authentication system failures
- Disk space critical (>95% full)
- Multiple failed login attempts (potential attack)

#### Warning Alerts (Business Hours Response)
- High response times (>3 seconds average)
- High resource utilization (>80% CPU/memory)
- Backup failures
- Certificate expiration warnings (<30 days)
- Performance degradation trends

#### Informational Alerts (Daily Review)
- User activity summaries
- System performance reports
- Security audit summaries
- Capacity planning recommendations

## Security and Compliance

### Access Controls

#### User Roles and Permissions
```yaml
roles:
  admin:
    permissions:
      - full_system_access
      - user_management
      - audit_log_access
      - configuration_changes
    
  editor:
    permissions:
      - document_upload
      - document_delete
      - query_all_documents
      - view_own_history
    
  viewer:
    permissions:
      - query_documents
      - view_own_history
      - download_responses
```

#### Network Security
- **External Access**: Only ports 80/443 exposed
- **Internal Segmentation**: Services isolated by function
- **TLS Everywhere**: All inter-service communication encrypted
- **Zero Trust**: All requests authenticated and authorized

### Audit and Compliance

#### Audit Trail Components
1. **User Actions**: Login/logout, document uploads, queries, downloads
2. **System Events**: Service starts/stops, configuration changes, errors
3. **Data Access**: Which documents accessed by whom and when
4. **Administrative Actions**: User role changes, system configuration

#### Compliance Reports
- **Weekly**: Security events summary, failed login attempts
- **Monthly**: User activity report, system performance summary  
- **Quarterly**: Full audit report, compliance attestation
- **Annual**: Security assessment, disaster recovery testing

### Backup and Recovery

#### Backup Strategy
```yaml
backup_schedule:
  database:
    frequency: "every 6 hours"
    retention: "90 days"
    encryption: "AES-256"
    
  vector_database:
    frequency: "daily"
    retention: "30 days"
    encryption: "AES-256"
    
  application_data:
    frequency: "daily"
    retention: "30 days"
    encryption: "AES-256"
    
  system_configuration:
    frequency: "weekly"
    retention: "1 year"
    encryption: "AES-256"
```

#### Recovery Procedures
- **RTO (Recovery Time Objective)**: 4 hours for full system restoration
- **RPO (Recovery Point Objective)**: 6 hours maximum data loss
- **Testing**: Monthly backup restoration testing
- **Documentation**: Complete disaster recovery runbooks

## Performance and Scaling

### Current Capacity
- **Concurrent Users**: 50 users simultaneously
- **Document Storage**: 10,000 documents, 100GB total
- **Query Load**: 1,000 queries per hour peak
- **Response Time**: <2 seconds average, <5 seconds 95th percentile

### Scaling Strategies

#### Horizontal Scaling
```yaml
scaling_options:
  anythingllm:
    current: 1 instance
    max: 3 instances
    trigger: "CPU > 70% for 5 minutes"
    
  ollama:
    current: 1 instance  
    max: 2 instances
    trigger: "Queue depth > 10"
    
  qdrant:
    current: 1 instance
    max: 3 instances (cluster mode)
    trigger: "Memory > 80%"
```

#### Vertical Scaling
- **Database**: Increase RAM for better query performance
- **Vector Store**: Add SSD storage for larger document collections
- **LLM Inference**: Add GPU resources for faster model inference

### Cost Analysis

#### Monthly Operating Costs (AWS/Azure equivalent)
- **Compute**: $800/month (16 cores, 32GB RAM)
- **Storage**: $200/month (200GB SSD + backup)
- **Monitoring**: $100/month (metrics and log retention)
- **SSL/Security**: $50/month (certificates and security tools)
- **Total**: ~$1,150/month

#### Cost Optimization Opportunities
- **Reserved Instances**: 30% savings on predictable compute
- **Storage Tiering**: 50% savings on long-term backup storage
- **Right-sizing**: 20% savings by optimizing instance sizes
- **Spot Instances**: Not recommended for production enterprise

## Success Metrics

### Technical Metrics
- **Availability**: 99.5% uptime during business hours
- **Performance**: 95% of queries complete within 3 seconds
- **Reliability**: Zero data loss incidents
- **Security**: Zero successful security breaches

### Business Metrics
- **User Adoption**: 80% of target users actively using system
- **Productivity**: 40% reduction in time to find information
- **Cost Efficiency**: ROI positive within 12 months
- **Compliance**: 100% audit compliance rating

## Lessons Learned

### Manifest System Benefits
1. **Complexity Management**: Enterprise features added without architectural redesign
2. **Security by Default**: Network segmentation and encryption automatically configured
3. **Operational Excellence**: Monitoring and backup systems included from day one
4. **Compliance Ready**: Audit logging and reporting built-in

### Operational Insights
1. **Monitoring First**: Comprehensive monitoring prevented multiple potential outages
2. **Security Layers**: Network segmentation contained a failed service without system impact
3. **Backup Validation**: Monthly restore testing caught backup corruption early
4. **User Training**: SSO integration required user education but improved security

---

*This enterprise example demonstrates how the Sushi Kitchen manifest system scales from simple development setups to production-grade enterprise systems while maintaining the same core functionality and adding comprehensive operational capabilities.*