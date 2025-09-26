# Deployment Guide

This guide provides detailed instructions for deploying Sushi Kitchen across different environments, from local development to enterprise production.

## Deployment Overview

Sushi Kitchen supports multiple deployment patterns to accommodate different use cases:

- **Local Development**: All services on a single machine
- **Small Team**: Integrated deployment with shared resources
- **Production**: Microservice architecture with proper isolation
- **Enterprise**: Kubernetes-based with high availability

## Prerequisites

### System Requirements

#### Minimum (Development)
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB free space
- **OS**: Linux, macOS, or Windows with WSL2

#### Recommended (Production)
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 100GB+ SSD
- **OS**: Linux (Ubuntu 20.04+, CentOS 8+, or RHEL 8+)

#### Enterprise (High Availability)
- **Nodes**: 3+ Kubernetes nodes
- **CPU**: 8+ cores per node
- **RAM**: 16GB+ per node
- **Storage**: 500GB+ distributed storage
- **Network**: Dedicated VPC with proper firewall rules

### Software Dependencies

```bash
# Core dependencies
docker >= 20.10
docker-compose >= 2.0
git >= 2.30
python >= 3.11
node >= 18 (for web frontend)

# Optional dependencies
kubectl >= 1.25 (for Kubernetes)
helm >= 3.10 (for Kubernetes charts)
```

## Local Development Deployment

### Single-Machine Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-org/sushi-kitchen.git
cd sushi-kitchen

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your preferences

# 3. Deploy the core stack
docker compose --profile hosomaki up -d

# 4. Deploy the API service (in separate terminal)
cd sushi-kitchen-api
docker compose -f docker-compose.api.yml up -d

# 5. Start the web frontend (in separate terminal)
cd sushi-kitchen-web
npm install
npm run dev
```

### Environment Configuration (.env)

```bash
# Database Configuration
POSTGRES_USER=sushi_user
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=sushi_kitchen
POSTGRES_PORT=5432

# Neo4j Configuration
NEO4J_USER=neo4j
NEO4J_PASSWORD=secure_neo4j_password
NEO4J_BOLT_PORT=7687
NEO4J_HTTP_PORT=7474

# API Configuration
SUSHI_API_PORT=8001
CORE_REPO_PATH=/path/to/sushi-kitchen

# Network Configuration
TZ=America/New_York

# Security (generate secure keys)
N8N_ENCRYPTION_KEY=$(openssl rand -base64 32)
GRAFANA_PASSWORD=admin_password

# Optional: Cloud Storage
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin123456
```

### Development Workflow

```bash
# Start core services
docker compose --profile hosomaki up -d

# Check service health
docker compose ps
docker compose logs -f api

# Generate a test configuration
curl -X POST "http://localhost:8001/api/v1/compose/generate" \
  -H "Content-Type: application/json" \
  -d '{"selection_type": "platter", "selection_id": "platter.hosomaki", "privacy_profile": "chirashi"}'

# Stop services
docker compose down
```

## Small Team Deployment

### Shared Development Environment

```yaml
# docker-compose.override.yml for team environment
version: '3.9'

services:
  # Expose services on known ports for team access
  postgres:
    ports:
      - "15432:5432"  # Non-conflicting port

  neo4j:
    ports:
      - "17474:7474"
      - "17687:7687"

  # Add persistent volumes for data
  postgres:
    volumes:
      - ./data/postgres:/var/lib/postgresql/data

  # Add team-specific monitoring
  grafana:
    environment:
      GF_SECURITY_ALLOW_EMBEDDING: "true"
      GF_AUTH_ANONYMOUS_ENABLED: "true"
    volumes:
      - ./config/grafana/team-dashboards:/var/lib/grafana/dashboards
```

### Team Environment Setup

```bash
# 1. Set up shared configuration
cat > .env.team <<EOF
POSTGRES_PASSWORD=${SHARED_DB_PASSWORD}
NEO4J_PASSWORD=${SHARED_NEO4J_PASSWORD}
GRAFANA_PASSWORD=${SHARED_MONITORING_PASSWORD}

# Use team-specific network
DOCKER_NETWORK_NAME=sushi_team_network
EOF

# 2. Deploy with team profile
docker compose --env-file .env.team --profile hosomaki --profile dragon up -d

# 3. Set up reverse proxy for external access
# nginx/traefik configuration for team.example.com
```

## Production Deployment

### Infrastructure Requirements

```bash
# Production server setup
# - Dedicated server or VPS
# - SSL certificates
# - Domain name
# - Backup strategy
# - Monitoring setup
```

### Production Docker Compose

```yaml
# docker-compose.production.yml
version: '3.9'

services:
  # Production-ready configurations
  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
      POSTGRES_DB: ${POSTGRES_DB}
    secrets:
      - postgres_password
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
      - ./backups/postgres:/backups
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3

  # API with production settings
  sushi-api:
    build:
      context: ./sushi-kitchen-api
      dockerfile: Dockerfile.production
    restart: always
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - CORE_REPO_PATH=/sushi-kitchen
    volumes:
      - ./:/sushi-kitchen:ro
      - api_logs:/var/log/sushi-api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M

  # Reverse proxy with SSL
  caddy:
    image: caddy:2
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/caddy/Caddyfile.production:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
  neo4j_password:
    file: ./secrets/neo4j_password.txt

volumes:
  postgres_data_prod:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/sushi-kitchen/data/postgres

  api_logs:
    driver: local
```

### Production SSL Configuration

```caddyfile
# Caddyfile.production
{
    email admin@example.com
}

sushi.example.com {
    reverse_proxy sushi-api:8000

    # Security headers
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
    }

    # Rate limiting
    rate_limit {
        zone static {
            key {remote_host}
            window 1m
            events 60
        }
    }
}

api.sushi.example.com {
    reverse_proxy sushi-api:8000 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}

monitoring.sushi.example.com {
    reverse_proxy grafana:3000

    # Basic auth for monitoring
    basicauth {
        admin $2a$10$...hashed_password...
    }
}
```

### Production Deployment Script

```bash
#!/bin/bash
# deploy-production.sh

set -euo pipefail

echo "🍣 Sushi Kitchen Production Deployment"

# Configuration
COMPOSE_FILE="docker-compose.production.yml"
ENV_FILE=".env.production"
BACKUP_DIR="/opt/backups/sushi-kitchen"

# Pre-deployment checks
echo "Running pre-deployment checks..."

# Check if required files exist
required_files=("$ENV_FILE" "$COMPOSE_FILE" "secrets/postgres_password.txt")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Required file missing: $file"
        exit 1
    fi
done

# Check Docker and docker-compose
docker --version || { echo "❌ Docker not found"; exit 1; }
docker compose version || { echo "❌ Docker Compose not found"; exit 1; }

# Check available disk space (require at least 10GB)
available_space=$(df . | awk 'NR==2 {print $4}')
if [[ $available_space -lt 10485760 ]]; then  # 10GB in KB
    echo "❌ Insufficient disk space. At least 10GB required."
    exit 1
fi

# Backup existing data
if [[ -d "postgres_data_prod" ]]; then
    echo "Creating backup of existing data..."
    timestamp=$(date +"%Y%m%d_%H%M%S")
    mkdir -p "$BACKUP_DIR"
    docker compose -f "$COMPOSE_FILE" exec postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/backup_$timestamp.sql"
fi

# Deploy
echo "Starting deployment..."
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d

# Health checks
echo "Running health checks..."
sleep 30

services=("postgres" "sushi-api" "caddy")
for service in "${services[@]}"; do
    if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "healthy\|running"; then
        echo "✅ $service is running"
    else
        echo "❌ $service failed to start"
        docker compose -f "$COMPOSE_FILE" logs "$service"
        exit 1
    fi
done

# API health check
if curl -f -s "http://localhost:8001/health" > /dev/null; then
    echo "✅ API health check passed"
else
    echo "❌ API health check failed"
    exit 1
fi

echo "🎉 Production deployment completed successfully!"
echo "🌐 Access your Sushi Kitchen at: https://sushi.example.com"
```

## Kubernetes Deployment

### Namespace and Resources

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: sushi-kitchen
  labels:
    name: sushi-kitchen
```

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sushi-config
  namespace: sushi-kitchen
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"
  TZ: "UTC"
```

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: sushi-secrets
  namespace: sushi-kitchen
type: Opaque
data:
  postgres-password: <base64-encoded-password>
  neo4j-password: <base64-encoded-password>
  grafana-password: <base64-encoded-password>
```

### Database Deployment

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: sushi-kitchen
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "sushi_kitchen"
        - name: POSTGRES_USER
          value: "sushi_user"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sushi-secrets
              key: postgres-password
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: sushi-kitchen
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

### API Deployment

```yaml
# k8s/api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sushi-api
  namespace: sushi-kitchen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sushi-api
  template:
    metadata:
      labels:
        app: sushi-api
    spec:
      containers:
      - name: sushi-api
        image: ghcr.io/your-org/sushi-kitchen-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: CORE_REPO_PATH
          value: "/sushi-kitchen"
        envFrom:
        - configMapRef:
            name: sushi-config
        volumeMounts:
        - name: core-repo
          mountPath: /sushi-kitchen
          readOnly: true
        - name: generated-files
          mountPath: /app/generated
          readOnly: true
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: core-repo
        configMap:
          name: core-repo-files
      - name: generated-files
        configMap:
          name: generated-bundle
      imagePullSecrets:
      - name: ghcr-secret

---
apiVersion: v1
kind: Service
metadata:
  name: sushi-api
  namespace: sushi-kitchen
spec:
  selector:
    app: sushi-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Ingress Configuration

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sushi-kitchen-ingress
  namespace: sushi-kitchen
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.sushi.example.com
    - sushi.example.com
    secretName: sushi-kitchen-tls
  rules:
  - host: api.sushi.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: sushi-api
            port:
              number: 80
  - host: sushi.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: sushi-web
            port:
              number: 80
```

### Helm Chart

```yaml
# helm/sushi-kitchen/values.yaml
replicaCount: 3

image:
  repository: ghcr.io/your-org/sushi-kitchen-api
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.sushi.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: sushi-kitchen-tls
      hosts:
        - api.sushi.example.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    username: sushi_user
    database: sushi_kitchen
  primary:
    persistence:
      enabled: true
      size: 20Gi

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
```

### Deployment Commands

```bash
# Deploy with kubectl
kubectl apply -f k8s/

# Deploy with Helm
helm install sushi-kitchen ./helm/sushi-kitchen \
  --namespace sushi-kitchen \
  --create-namespace \
  --values ./helm/values-production.yaml

# Monitor deployment
kubectl get pods -n sushi-kitchen -w

# Check logs
kubectl logs -f deployment/sushi-api -n sushi-kitchen

# Scale deployment
kubectl scale deployment sushi-api --replicas=5 -n sushi-kitchen
```

## Monitoring and Maintenance

### Health Checks

```bash
#!/bin/bash
# health-check.sh

API_URL="https://api.sushi.example.com"

# Check API health
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
if [[ $response == "200" ]]; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed (HTTP $response)"
    exit 1
fi

# Check database connectivity
db_check=$(curl -s "$API_URL/health" | jq -r '.checks.database')
if [[ $db_check == "true" ]]; then
    echo "✅ Database is accessible"
else
    echo "❌ Database check failed"
fi

# Check bundle generation
bundle_check=$(curl -s "$API_URL/api/v1/bundle" | jq -r '.version' 2>/dev/null)
if [[ -n $bundle_check && $bundle_check != "null" ]]; then
    echo "✅ Bundle is available (version: $bundle_check)"
else
    echo "⚠️  Bundle check failed"
fi
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups/sushi-kitchen"
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

# Database backup
docker compose exec postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sql.gz"

# Configuration backup
tar -czf "$BACKUP_DIR/config_$(date +%Y%m%d_%H%M%S).tar.gz" \
    .env* \
    config/ \
    docs/manifest/

# Clean old backups
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete
```

### Log Management

```bash
# Configure log rotation
cat > /etc/logrotate.d/sushi-kitchen <<EOF
/opt/sushi-kitchen/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

# Monitor logs
docker compose logs -f --tail=100 sushi-api
```

This deployment guide provides comprehensive instructions for deploying Sushi Kitchen across different environments, from development to enterprise production with Kubernetes.