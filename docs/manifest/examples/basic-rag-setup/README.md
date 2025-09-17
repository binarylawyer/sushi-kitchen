# 🍣 Basic RAG Setup Example

*A complete walkthrough showing how the Sushi Kitchen manifest system transforms a simple user goal into a working document question-answering system*

## User Story

**Goal**: "I want to upload documents and ask questions about them using local AI models."

**User Knowledge Level**: Beginner - understands Docker basics but not AI infrastructure complexity

**Time Investment**: 30 minutes setup + 15 minutes validation = 45 minutes total

## What This Example Demonstrates

This example showcases the core value proposition of the Sushi Kitchen manifest system: **intelligent dependency resolution**. The user expresses a high-level goal, and the system automatically determines all the required technical components, their configurations, and how they should connect together.

### The Complexity Hidden From The User

Behind the simple goal of "chat with documents" lies significant technical complexity:
- **LLM Inference**: Running large language models locally for question answering
- **Vector Storage**: Converting documents into searchable embeddings  
- **Database Storage**: Managing user sessions, chat history, and document metadata
- **Document Processing**: Parsing PDFs, text files, and other document formats
- **Web Interface**: Providing a user-friendly chat interface
- **Dependency Resolution**: Ensuring all services can communicate properly
- **Resource Management**: Configuring appropriate CPU, memory, and storage limits
- **Network Configuration**: Setting up Docker networking for service discovery

The manifest system handles all of this automatically based on the user's service selection.

## User's Selection Process

### Step 1: Browse Available Combos

The user browses `core/menu-manifest.md` and discovers the "Local Chat" combo:

```yaml
- id: combo.chat-local
  name: "Local Chat" 
  description: "The simplest possible setup for chatting with local AI models..."
  includes: ["hosomaki.ollama", "hosomaki.anythingllm"]
```

### Step 2: Understand Service Characteristics

The user sees helpful badges that communicate important information:
- **Ollama**: `popular`, `gpu-optional` - widely used, works better with GPU but not required
- **AnythingLLM**: `popular`, `battle-tested` - proven RAG interface with good community support

### Step 3: Check Resource Requirements

The combo indicates resource estimates:
- **CPU**: 2-4 cores recommended  
- **Memory**: 4-8 GB required
- **Storage**: 10-25 GB for models and data
- **GPU**: Optional but recommended for better performance

### Step 4: Select the Combo

User decides this meets their needs and selects `combo.chat-local` for deployment.

## Manifest System Processing

### Dependency Resolution Process

When the user selects the "Local Chat" combo, here's what happens behind the scenes:

#### 1. Service Analysis
```yaml
# User selected services:
- hosomaki.ollama      # Provides: local_llm_inference
- hosomaki.anythingllm # Requires: local_llm_inference, vector_storage, relational_storage
```

#### 2. Capability Matching
The system analyzes capabilities:
- ✅ AnythingLLM needs `local_llm_inference` → Ollama provides this
- ❌ AnythingLLM needs `vector_storage` → Not satisfied
- ❌ AnythingLLM needs `relational_storage` → Not satisfied

#### 3. Automatic Dependency Addition
The system automatically adds required services:
- Adds `futomaki.qdrant` for vector storage (default provider)
- Adds `futomaki.postgresql` for relational storage (default provider)

#### 4. Final Service List
```yaml
Final deployment includes:
- hosomaki.ollama        # User selected
- hosomaki.anythingllm   # User selected  
- futomaki.qdrant        # Auto-added for vector storage
- futomaki.postgresql    # Auto-added for relational storage
```

### Configuration Generation

The system then generates appropriate configurations for each service:

#### Network Configuration
Using `open_research` privacy profile (development-friendly):
- Single `sushi_net` bridge network
- All services can communicate using service names as hostnames
- External ports exposed for user access

#### Environment Variables
Using `development` environment template:
- Debug logging enabled for troubleshooting
- Relaxed security for local development
- Shorter timeouts for faster feedback

#### Resource Allocation
Based on service contracts and user's hardware:
- Ollama: 2 CPU cores, 4GB RAM, 50GB storage  
- AnythingLLM: 1 CPU core, 2GB RAM, 10GB storage
- Qdrant: 1 CPU core, 2GB RAM, 20GB storage
- PostgreSQL: 1 CPU core, 1GB RAM, 10GB storage

## Generated Docker Compose Configuration

The manifest system produces this complete `docker-compose.yml`:

```yaml
version: '3.9'

# Metadata for tracking and management
x-sushi-metadata:
  labels:
    - "sushi.kitchen.generated=true"
    - "sushi.kitchen.combo-ids=combo.chat-local"
    - "sushi.kitchen.privacy-profile=open_research"
    - "sushi.kitchen.environment-template=development"

services:
  # Local LLM inference engine
  ollama:
    image: ollama/ollama:latest
    container_name: sushi_ollama
    profiles: ["hosomaki"]
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_KEEP_ALIVE=5m
      - OLLAMA_DEBUG=true
    networks:
      - sushi_net
    restart: unless-stopped
    
  # Document chat interface  
  anythingllm:
    image: mintplexlabs/anythingllm:latest
    container_name: sushi_anythingllm
    profiles: ["hosomaki"]
    ports:
      - "3001:3001"
    volumes:
      - anythingllm_storage:/app/server/storage
      - anythingllm_hotdir:/app/collector/hotdir
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_PATH=http://ollama:11434
      - VECTOR_DB=qdrant  
      - QDRANT_ENDPOINT=http://qdrant:6333
      - DATABASE_URL=postgresql://anythingllm:${POSTGRES_PASSWORD}@postgresql:5432/anythingllm
    depends_on:
      - ollama
      - qdrant
      - postgresql
    networks:
      - sushi_net
    restart: unless-stopped

  # Vector database for document embeddings
  qdrant:
    image: qdrant/qdrant:latest
    container_name: sushi_qdrant
    profiles: ["futomaki"]
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__LOG_LEVEL=debug
      - QDRANT__SERVICE__ENABLE_CORS=true
    networks:
      - sushi_net
    restart: unless-stopped

  # PostgreSQL for application data
  postgresql:
    image: postgres:15-alpine
    container_name: sushi_postgresql
    profiles: ["futomaki"] 
    ports:
      - "5432:5432"
    volumes:
      - postgresql_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=anythingllm
      - POSTGRES_USER=anythingllm
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_LOG_STATEMENT=all
    networks:
      - sushi_net
    restart: unless-stopped

networks:
  sushi_net:
    driver: bridge
    ipam:
      config:
        - subnet: "172.20.0.0/16"

volumes:
  ollama_data:
    driver: local
  anythingllm_storage:
    driver: local
  anythingllm_hotdir:
    driver: local
  qdrant_storage:
    driver: local
  postgresql_data:
    driver: local
```

## Step-by-Step Deployment Guide

### Prerequisites

Before starting, ensure you have:
- Docker and Docker Compose installed
- At least 8GB RAM available
- 50GB free disk space
- (Optional) NVIDIA GPU with drivers for better performance

### Deployment Steps

#### 1. Generate Configuration
```bash
# Using the manifest system (conceptual - actual implementation would vary)
sushi-kitchen generate --combo chat-local --profile development
```

#### 2. Set Required Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Set database password
export POSTGRES_PASSWORD="your-secure-password-here"
```

#### 3. Start the System
```bash
# Start all services
docker-compose up -d

# Monitor startup progress
docker-compose logs -f
```

#### 4. Download Initial Models
```bash
# Download a recommended model for chat
docker-compose exec ollama ollama pull llama3.2:3b

# Verify model is available
docker-compose exec ollama ollama list
```

### Expected Startup Sequence

The services start in dependency order:

1. **PostgreSQL** (0-30 seconds)
   - Database initializes and creates required schemas
   - Health check confirms database is accepting connections

2. **Qdrant** (0-15 seconds)  
   - Vector database starts and initializes storage
   - REST API becomes available on port 6333

3. **Ollama** (0-60 seconds)
   - LLM inference engine starts
   - API becomes available on port 11434
   - Ready to load and run models

4. **AnythingLLM** (30-90 seconds)
   - Connects to PostgreSQL for application data
   - Connects to Qdrant for vector storage
   - Connects to Ollama for LLM inference
   - Web interface becomes available on port 3001

### Troubleshooting Common Issues

#### Issue: Services Can't Connect
**Symptoms**: AnythingLLM shows connection errors in logs
**Solution**: 
```bash
# Check all services are running
docker-compose ps

# Verify network connectivity
docker-compose exec anythingllm ping ollama
docker-compose exec anythingllm ping qdrant
```

#### Issue: Ollama Can't Load Models
**Symptoms**: Out of memory errors when loading models
**Solution**:
```bash
# Check available memory
docker stats

# Try a smaller model
docker-compose exec ollama ollama pull llama3.2:1b
```

#### Issue: Slow Response Times
**Symptoms**: Long delays when asking questions
**Solutions**:
- Enable GPU acceleration if available
- Use smaller models for faster inference
- Increase memory allocation for Ollama

## Validation and Success Criteria

### System Health Checks

#### 1. Service Availability
```bash
# All services should be running
docker-compose ps
# Expected: All services show "Up" status

# Check service health
curl http://localhost:11434/api/tags        # Ollama API
curl http://localhost:6333/health           # Qdrant health
curl http://localhost:3001/api/system       # AnythingLLM API
```

#### 2. Inter-Service Communication
```bash
# Verify AnythingLLM can reach dependencies
docker-compose exec anythingllm curl http://ollama:11434/api/tags
docker-compose exec anythingllm curl http://qdrant:6333/health
```

#### 3. Database Connectivity
```bash
# Verify PostgreSQL connection
docker-compose exec postgresql psql -U anythingllm -d anythingllm -c "SELECT version();"
```

### Functional Testing

#### 1. Access Web Interface
- Navigate to http://localhost:3001
- Interface should load without errors
- Setup wizard should guide initial configuration

#### 2. Upload and Process Documents
- Upload a test PDF or text file
- Verify document appears in document list
- Check that processing completes successfully

#### 3. Chat Functionality
- Ask a question about the uploaded document
- Verify response is relevant and accurate
- Check that conversation history is preserved

#### 4. Model Management
- Access model settings in AnythingLLM
- Verify Ollama connection is working
- Test switching between different models

### Performance Validation

#### 1. Response Time Testing
```bash
# Test basic response times
time curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:3b", "prompt": "Hello, how are you?", "stream": false}'
```

#### 2. Resource Usage Monitoring
```bash
# Monitor resource consumption
docker stats --no-stream

# Expected resource usage:
# - Total RAM: 6-8GB
# - Total CPU: 2-4 cores active
# - Network: Minimal unless actively processing
```

#### 3. Storage Verification
```bash
# Check volume usage
docker system df -v

# Verify data persistence
docker-compose restart
# Uploaded documents should remain after restart
```

## Learning Outcomes

### What Users Learn

By completing this example, users understand:

1. **Service Dependencies**: How AI applications require multiple coordinated services
2. **Automatic Resolution**: How the manifest system eliminates manual dependency management  
3. **Configuration Management**: How environment templates optimize settings for different contexts
4. **Resource Planning**: How to estimate and allocate hardware resources appropriately
5. **Validation Strategies**: How to verify that complex systems are working correctly

### Manifest System Capabilities Demonstrated

This example showcases:

1. **Intelligent Dependency Resolution**: Automatically adding required services
2. **Configuration Generation**: Creating optimized Docker Compose configurations
3. **Resource Management**: Allocating appropriate resources based on service requirements
4. **Network Setup**: Configuring Docker networking for service discovery
5. **Environment Adaptation**: Applying development-optimized settings automatically

## Next Steps

### Expanding the System

Users can evolve this basic setup by:

1. **Adding Monitoring**: Include `inari.prometheus` and `inari.grafana` for system visibility
2. **Enhancing Security**: Switch to `business_confidential` privacy profile
3. **Scaling Up**: Move to `bento.knowledge-powerhouse` for more comprehensive capabilities
4. **Production Deployment**: Apply `production` environment template with proper security

### Related Examples

- **enterprise-deployment/**: Shows this same RAG system with enterprise security and monitoring
- **compliance-ready/**: Demonstrates HIPAA/GDPR-ready deployment of document processing

## Architecture Insights

### Why These Services Work Well Together

The manifest system selected these specific services because:

1. **Ollama + AnythingLLM**: Proven integration with extensive community testing
2. **Qdrant + AnythingLLM**: High-performance vector search optimized for RAG workloads  
3. **PostgreSQL + AnythingLLM**: Reliable relational storage for application data
4. **Development Profile**: Debug-friendly settings for learning and experimentation

### Scalability Considerations

This basic setup can handle:
- **Documents**: 100-1000 documents depending on size
- **Concurrent Users**: 2-5 simultaneous users
- **Query Volume**: 50-100 queries per hour
- **Model Size**: Up to 7B parameter models on 16GB+ systems

For larger requirements, the manifest system can suggest upgrades to more powerful combinations or distributed architectures.

---

*This example demonstrates the core value of the Sushi Kitchen manifest system: transforming complex AI infrastructure deployment into simple, reliable, and understandable processes that just work.*