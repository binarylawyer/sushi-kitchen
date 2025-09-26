from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from .orchestrators.manifest_orchestrator import ManifestOrchestrator
from .models import (
    GenerateRequest,
    GenerateResponse,
    AvailableComponentsResponse,
    HealthResponse,
    ComponentInfo
)
import os
import yaml
import asyncio
from pathlib import Path
from typing import Dict, List

app = FastAPI(
    title="Sushi Kitchen API",
    version="1.0.0",
    description="API for generating Docker Compose configurations from Sushi Kitchen manifests",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://sushi-kitchen.dev", "*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize orchestrator
core_repo_path = os.getenv("CORE_REPO_PATH", "/app")  # Path to mounted sushi-kitchen repo
orchestrator = ManifestOrchestrator(core_repo_path)

@app.post("/api/v1/compose/generate", response_model=GenerateResponse)
async def generate_compose(request: GenerateRequest):
    """Generate Docker Compose configuration"""
    try:
        # Generate the complete stack
        result_dict = await orchestrator.generate_complete_stack(
            selection_type=request.selection_type,
            selection_id=request.selection_id,
            profile=request.privacy_profile,
            include_optional=request.include_optional
        )

        # Convert to YAML
        result_yaml = yaml.dump(result_dict, default_flow_style=False, sort_keys=False)

        # Validate the configuration
        validation = await orchestrator.validate_configuration(result_dict)

        return GenerateResponse(
            yaml=result_yaml,
            services=list(result_dict.get('services', {}).keys()),
            profile=request.privacy_profile,
            success=True,
            validation=validation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/api/v1/components", response_model=AvailableComponentsResponse)
async def get_available_components():
    """Get all available platters, combos, and rolls"""
    try:
        components = await orchestrator.get_available_components()

        # Convert to response format
        platters = [
            ComponentInfo(
                id=platter_id,
                name=platter_data.get('name', ''),
                description=platter_data.get('description', ''),
                tags=platter_data.get('tags', []),
                difficulty=platter_data.get('difficulty'),
                estimated_setup_time_min=platter_data.get('estimated_setup_time_min')
            )
            for platter_id, platter_data in components.get('platters', {}).items()
        ]

        combos = [
            ComponentInfo(
                id=combo_id,
                name=combo_data.get('name', ''),
                description=combo_data.get('description', ''),
                tags=combo_data.get('tags', []),
                difficulty=combo_data.get('difficulty'),
                estimated_setup_time_min=combo_data.get('estimated_setup_time_min')
            )
            for combo_id, combo_data in components.get('combos', {}).items()
        ]

        rolls = {
            roll_id: ComponentInfo(
                id=roll_id,
                name=roll_data.get('name', ''),
                description=roll_data.get('description', ''),
                category=roll_data.get('category', ''),
                tags=roll_data.get('tags', [])
            )
            for roll_id, roll_data in components.get('rolls', {}).items()
        }

        return AvailableComponentsResponse(
            platters=platters,
            combos=combos,
            rolls=rolls,
            capabilities=components.get('capabilities', {}),
            network_profiles=components.get('network_profiles', {})
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load components: {str(e)}")

@app.get("/api/v1/components/platter/{platter_id}")
async def get_platter_details(platter_id: str):
    """Get detailed information about a specific platter"""
    try:
        components = await orchestrator.get_available_components()
        platter = components.get('platters', {}).get(platter_id)

        if not platter:
            raise HTTPException(status_code=404, detail=f"Platter '{platter_id}' not found")

        return platter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get platter details: {str(e)}")

@app.get("/api/v1/components/combo/{combo_id}")
async def get_combo_details(combo_id: str):
    """Get detailed information about a specific combo"""
    try:
        components = await orchestrator.get_available_components()
        combo = components.get('combos', {}).get(combo_id)

        if not combo:
            raise HTTPException(status_code=404, detail=f"Combo '{combo_id}' not found")

        return combo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get combo details: {str(e)}")

@app.post("/api/v1/compose/validate")
async def validate_compose(compose_yaml: str):
    """Validate a Docker Compose YAML configuration"""
    try:
        # Parse YAML
        compose_dict = yaml.safe_load(compose_yaml)

        # Validate
        validation = await orchestrator.validate_configuration(compose_dict)

        return validation
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    core_repo_accessible = Path(core_repo_path).exists()

    scripts_available = {
        'generate-compose': (Path(core_repo_path) / 'scripts' / 'generate-compose.py').exists(),
        'generate-network-config': (Path(core_repo_path) / 'scripts' / 'generate-network-config.py').exists(),
        'export-manifest': (Path(core_repo_path) / 'scripts' / 'export-manifest-json.py').exists(),
    }

    bundle_info = None
    try:
        # Try to get basic component info
        components = await orchestrator.get_available_components()
        bundle_info = {
            'platters_count': len(components.get('platters', {})),
            'combos_count': len(components.get('combos', {})),
            'rolls_count': len(components.get('rolls', {}))
        }
    except Exception:
        pass  # Bundle info is optional for health check

    overall_status = "healthy" if core_repo_accessible and all(scripts_available.values()) else "degraded"

    return HealthResponse(
        status=overall_status,
        core_repo_accessible=core_repo_accessible,
        scripts_available=scripts_available,
        bundle_info=bundle_info
    )

@app.get("/api/v1/network-profiles")
async def get_network_profiles():
    """Get available network security profiles"""
    profiles = {
        'chirashi': {
            'name': 'Research/Development',
            'description': 'Single network for research and development use',
            'security_level': 'low',
            'suitable_for': ['development', 'research', 'learning']
        },
        'temaki': {
            'name': 'Business/Production',
            'description': 'Segmented networks for business production use',
            'security_level': 'medium',
            'suitable_for': ['business', 'production', 'small-team']
        },
        'inari': {
            'name': 'Enterprise/Compliance',
            'description': 'Multi-tier isolated networks for enterprise compliance',
            'security_level': 'high',
            'suitable_for': ['enterprise', 'compliance', 'high-security']
        }
    }
    return profiles

@app.get("/api/v1/types/typescript", response_class=PlainTextResponse)
async def get_typescript_types():
    """Get TypeScript type definitions"""
    types_path = Path(__file__).parent.parent / 'generated' / 'types' / 'sushi-kitchen.ts'

    # Also check Docker mount point
    if not types_path.exists():
        types_path = Path('/app/generated/types/sushi-kitchen.ts')

    if not types_path.exists():
        raise HTTPException(status_code=404, detail="TypeScript types not found. Run CI/CD pipeline to generate.")

    try:
        with types_path.open() as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read types: {str(e)}")

@app.get("/api/v1/bundle")
async def get_api_bundle():
    """Get the raw API bundle JSON"""
    bundle_path = Path(__file__).parent.parent / 'generated' / 'api-bundle.json'

    # Also check Docker mount point
    if not bundle_path.exists():
        bundle_path = Path('/app/generated/api-bundle.json')

    if not bundle_path.exists():
        raise HTTPException(status_code=404, detail="API bundle not found. Run CI/CD pipeline to generate.")

    try:
        with bundle_path.open() as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bundle: {str(e)}")

# Admin endpoints (for CI/CD integration)
@app.post("/admin/cache/refresh")
async def refresh_cache(background_tasks: BackgroundTasks, bundle_url: str = None):
    """Refresh cached manifest data (for CI/CD integration)"""
    # This would typically be protected by authentication
    # For now, just return success
    background_tasks.add_task(lambda: print(f"Cache refresh requested for {bundle_url}"))
    return {"status": "refresh_scheduled", "bundle_url": bundle_url}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")