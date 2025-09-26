from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GenerateRequest(BaseModel):
    selection_type: str = Field(..., description="Type of selection: platter, combo, or roll")
    selection_id: str = Field(..., description="ID of the selected component")
    privacy_profile: str = Field(default="chirashi", description="Network security profile")
    include_optional: bool = Field(default=False, description="Include optional components")

class ValidationResult(BaseModel):
    valid: bool
    warnings: List[str] = []
    errors: List[str] = []

class GenerateResponse(BaseModel):
    yaml: str = Field(..., description="Generated Docker Compose YAML")
    services: List[str] = Field(..., description="List of included service names")
    profile: str = Field(..., description="Applied network security profile")
    success: bool = Field(..., description="Whether generation was successful")
    validation: Optional[ValidationResult] = None

class ComponentInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    difficulty: Optional[str] = None
    estimated_setup_time_min: Optional[int] = None

class AvailableComponentsResponse(BaseModel):
    platters: List[ComponentInfo]
    combos: List[ComponentInfo]
    rolls: Dict[str, ComponentInfo]
    capabilities: Dict[str, Any]
    network_profiles: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    core_repo_accessible: bool
    scripts_available: Dict[str, bool]
    bundle_info: Optional[Dict[str, Any]] = None