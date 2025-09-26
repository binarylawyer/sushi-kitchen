# 🍣 Sushi Kitchen API

FastAPI backend service for the Sushi Kitchen platform. This API orchestrates the core generation scripts and provides web-accessible endpoints for creating Docker Compose configurations.

## Architecture

This API service is part of the 3-repo Sushi Kitchen architecture:
- **sushi-kitchen** - Core manifests, scripts, and generation logic (single source of truth)
- **sushi-kitchen-api** - FastAPI backend service (this repo)
- **sushi-kitchen-web** - Frontend and website

## Features

- **Compose Generation**: Generate Docker Compose files from platters, combos, or individual rolls
- **Network Security**: Apply network security profiles (chirashi/temaki/inari)
- **Component Discovery**: Browse available components and their dependencies
- **Validation**: Validate generated configurations
- **TypeScript Types**: Auto-generated type definitions for frontend integration

## API Endpoints

### Core Endpoints
- `POST /api/v1/compose/generate` - Generate Docker Compose configuration
- `GET /api/v1/components` - List all available components
- `GET /api/v1/components/platter/{id}` - Get platter details
- `GET /api/v1/components/combo/{id}` - Get combo details
- `GET /api/v1/network-profiles` - List network security profiles
- `POST /api/v1/compose/validate` - Validate compose configuration

### System Endpoints
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `POST /admin/cache/refresh` - Refresh cached data (CI/CD integration)

## Directory Structure

```
sushi-kitchen-api/
├── app/                          # FastAPI application
│   ├── main.py                   # Main FastAPI app
│   ├── models.py                 # Pydantic models
│   └── orchestrators/
│       └── manifest_orchestrator.py  # Core logic orchestrator
├── generated/                    # Generated files (created by CI/CD)
│   ├── api-bundle.json          # API bundle with all components
│   └── types/
│       └── sushi-kitchen.ts     # TypeScript type definitions
├── docker-compose.api.yml       # Standalone deployment
├── Dockerfile                   # Container definition
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Running the API

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable to point to core repo
export CORE_REPO_PATH=/path/to/sushi-kitchen

# Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Mode
```bash
# Build and run with docker-compose
docker-compose -f docker-compose.api.yml up --build

# Or set custom core repo path
CORE_REPO_PATH=/custom/path/to/sushi-kitchen docker-compose -f docker-compose.api.yml up
```

### Production Deployment
The API is designed to be deployed alongside the main sushi-kitchen repository:

```bash
# Assuming both repos are in the same directory
/projects/
├── sushi-kitchen/          # Main repo with manifests and scripts
└── sushi-kitchen-api/      # This API repo

# Run from the API directory
docker-compose -f docker-compose.api.yml up -d
```

## Environment Variables

- `CORE_REPO_PATH` - Path to the main sushi-kitchen repository (default: `/sushi-kitchen`)
- `SUSHI_API_PORT` - API port (default: `8001`)

## Integration with Main Repo

The API depends on the main `sushi-kitchen` repository for:
- Core generation scripts (`scripts/generate-compose.py`, etc.)
- Manifest files (`docs/manifest/`)
- Network configuration scripts

The CI/CD pipeline in the main repo generates:
- `generated/api-bundle.json` - Complete component bundle
- `generated/types/sushi-kitchen.ts` - TypeScript definitions

## Development Notes

- The API mounts the core repo as read-only
- All generation happens via subprocess calls to the core scripts
- Generated files are created in a temporary directory
- The orchestrator handles network security overlays and validation
- TypeScript types are auto-generated from the API bundle

## API Examples

### Generate a Basic Compose File
```bash
curl -X POST "http://localhost:8001/api/v1/compose/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "selection_type": "platter",
    "selection_id": "platter.hosomaki",
    "privacy_profile": "chirashi",
    "include_optional": false
  }'
```

### Get Available Components
```bash
curl "http://localhost:8001/api/v1/components"
```

### Health Check
```bash
curl "http://localhost:8001/health"
```