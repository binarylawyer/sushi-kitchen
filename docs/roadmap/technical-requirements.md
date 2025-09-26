# Technical Requirements & Implementation Specifications

This document provides detailed technical specifications for implementing the remaining 20% of functionality needed to achieve the target user experience.

## 🏗️ Infrastructure Requirements

### **Supabase Configuration**

#### Project Setup
```bash
# Supabase CLI setup
npx supabase init
npx supabase start
npx supabase db reset

# Environment variables needed
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
DATABASE_URL=postgresql://postgres:password@localhost:54322/postgres
```

#### Authentication Configuration
```sql
-- Enable email authentication
INSERT INTO auth.providers (id, name, enabled) VALUES
  ('email', 'Email', true),
  ('google', 'Google OAuth', true),
  ('github', 'GitHub OAuth', true);

-- Configure auth settings
UPDATE auth.config SET
  site_url = 'http://localhost:3000',
  jwt_exp = 3600,
  refresh_token_rotation_enabled = true,
  security_update_password_require_reauthentication = true;
```

#### Storage Buckets
```sql
-- Create storage bucket for user uploads (future use)
INSERT INTO storage.buckets (id, name, public) VALUES
  ('user-configs', 'user-configs', false),
  ('public-assets', 'public-assets', true);

-- Set up storage policies
CREATE POLICY "Users can upload own configs" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'user-configs' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### **Database Schema Implementation**

#### Complete Schema with Indexes
```sql
-- Users and Authentication
CREATE TABLE user_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    organization TEXT,
    tier TEXT DEFAULT 'free' CHECK (tier IN ('free', 'pro', 'enterprise')),
    api_key TEXT UNIQUE DEFAULT encode(gen_random_bytes(32), 'base64'),
    monthly_generations INTEGER DEFAULT 0,
    max_monthly_generations INTEGER DEFAULT 100,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Saved Configurations
CREATE TABLE saved_configurations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    selection_type TEXT NOT NULL CHECK (selection_type IN ('platter', 'combo', 'roll', 'custom')),
    selection_id TEXT NOT NULL,
    privacy_profile TEXT NOT NULL CHECK (privacy_profile IN ('chirashi', 'temaki', 'inari')),
    include_optional BOOLEAN DEFAULT FALSE,
    generated_config JSONB NOT NULL,
    config_hash TEXT NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    is_template BOOLEAN DEFAULT FALSE,
    tags TEXT[] DEFAULT '{}',
    download_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    fork_count INTEGER DEFAULT 0,
    parent_config_id UUID REFERENCES saved_configurations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Generation History for Analytics
CREATE TABLE generation_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    configuration_id UUID REFERENCES saved_configurations(id) ON DELETE SET NULL,
    selection_type TEXT NOT NULL,
    selection_id TEXT NOT NULL,
    privacy_profile TEXT NOT NULL,
    include_optional BOOLEAN DEFAULT FALSE,
    generation_source TEXT NOT NULL CHECK (generation_source IN ('prebuilt', 'custom', 'cached')),
    generation_time INTERVAL,
    response_size INTEGER,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    error_code TEXT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Configuration Popularity Tracking
CREATE TABLE configuration_popularity (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    selection_type TEXT NOT NULL,
    selection_id TEXT NOT NULL,
    privacy_profile TEXT NOT NULL,
    include_optional BOOLEAN DEFAULT FALSE,
    generation_count INTEGER DEFAULT 1,
    unique_users_count INTEGER DEFAULT 1,
    last_generated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    trend_score FLOAT DEFAULT 0.0,
    UNIQUE(selection_type, selection_id, privacy_profile, include_optional)
);

-- User Configuration Likes/Bookmarks
CREATE TABLE configuration_interactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    configuration_id UUID REFERENCES saved_configurations(id) ON DELETE CASCADE,
    interaction_type TEXT NOT NULL CHECK (interaction_type IN ('like', 'bookmark', 'fork')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, configuration_id, interaction_type)
);

-- Teams and Organizations (Enterprise)
CREATE TABLE organizations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    tier TEXT DEFAULT 'team' CHECK (tier IN ('team', 'enterprise')),
    max_members INTEGER DEFAULT 10,
    max_monthly_generations INTEGER DEFAULT 1000,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE organization_members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

-- Indexes for Performance
CREATE INDEX idx_saved_configurations_user_id ON saved_configurations(user_id);
CREATE INDEX idx_saved_configurations_public ON saved_configurations(is_public) WHERE is_public = true;
CREATE INDEX idx_saved_configurations_tags ON saved_configurations USING GIN(tags);
CREATE INDEX idx_generation_history_user_id_created ON generation_history(user_id, created_at DESC);
CREATE INDEX idx_configuration_popularity_trend ON configuration_popularity(trend_score DESC, generation_count DESC);
CREATE INDEX idx_configuration_interactions_user ON configuration_interactions(user_id, interaction_type);

-- Functions for automatic updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_saved_configurations_updated_at BEFORE UPDATE ON saved_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### Row Level Security Policies
```sql
-- User Profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = id);

-- Saved Configurations
ALTER TABLE saved_configurations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own configurations" ON saved_configurations
    FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Anyone can view public configurations" ON saved_configurations
    FOR SELECT USING (is_public = true);

-- Generation History
ALTER TABLE generation_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own history" ON generation_history
    FOR SELECT USING (auth.uid() = user_id);

-- Configuration Interactions
ALTER TABLE configuration_interactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own interactions" ON configuration_interactions
    FOR ALL USING (auth.uid() = user_id);

-- Organizations (Enterprise)
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Organization members can view org" ON organizations
    FOR SELECT USING (
        id IN (
            SELECT organization_id FROM organization_members
            WHERE user_id = auth.uid()
        )
    );

ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Members can view org membership" ON organization_members
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM organization_members
            WHERE user_id = auth.uid()
        )
    );
```

## 🔧 API Implementation Details

### **Enhanced FastAPI Application Structure**

```python
# sushi-kitchen-api/app/main.py - Updated structure
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from .auth.middleware import get_current_user, check_rate_limit, optional_auth
from .routes import (
    auth_routes,
    configurations_routes,
    generation_routes,
    dashboard_routes,
    admin_routes,
    public_routes
)
from .services import (
    prebuilt_service,
    analytics_service,
    notification_service
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sushi Kitchen API",
    version="2.0.0",
    description="Complete API for Sushi Kitchen platform with user management",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])  # Configure for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://sushi-kitchen.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s"
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include route modules
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(generation_routes.router, prefix="/api/v1/compose", tags=["generation"])
app.include_router(configurations_routes.router, prefix="/api/v1/configurations", tags=["configurations"])
app.include_router(dashboard_routes.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(public_routes.router, prefix="/api/v1/public", tags=["public"])
app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["admin"])

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

# Health check with dependency verification
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    checks = {
        "api": True,
        "database": await check_database_connection(),
        "supabase": await check_supabase_connection(),
        "core_repo": check_core_repo_access(),
        "prebuilt_cache": await prebuilt_service.health_check()
    }

    healthy = all(checks.values())

    return {
        "status": "healthy" if healthy else "degraded",
        "checks": checks,
        "timestamp": time.time(),
        "version": "2.0.0"
    }
```

### **Authentication and Authorization System**

```python
# sushi-kitchen-api/app/auth/middleware.py - Complete implementation
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
from functools import wraps
import os
import jwt
from datetime import datetime, timedelta
import redis

# Initialize clients
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
security = HTTPBearer()

class UserTier:
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

TIER_LIMITS = {
    UserTier.FREE: {
        "monthly_generations": 100,
        "saved_configurations": 10,
        "public_configurations": 3
    },
    UserTier.PRO: {
        "monthly_generations": 1000,
        "saved_configurations": 100,
        "public_configurations": 20
    },
    UserTier.ENTERPRISE: {
        "monthly_generations": 10000,
        "saved_configurations": 1000,
        "public_configurations": 100
    }
}

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Extract and validate user from JWT token"""
    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        if not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Get or create user profile
        profile_result = supabase.table('user_profiles')\
            .select('*')\
            .eq('id', user.user.id)\
            .execute()

        if not profile_result.data:
            # Create profile for new user
            profile_data = {
                'id': user.user.id,
                'email': user.user.email,
                'full_name': user.user.user_metadata.get('full_name', ''),
                'tier': UserTier.FREE
            }

            create_result = supabase.table('user_profiles')\
                .insert(profile_data)\
                .execute()

            profile = create_result.data[0]
        else:
            profile = profile_result.data[0]

        return {
            'id': user.user.id,
            'email': user.user.email,
            'profile': profile,
            'tier': profile['tier']
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

async def optional_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    """Optional authentication for public endpoints"""
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

async def check_rate_limit(user = Depends(get_current_user)):
    """Check rate limits based on user tier"""
    profile = user['profile']
    tier_limits = TIER_LIMITS[profile['tier']]

    # Check monthly generation limit
    if profile['monthly_generations'] >= tier_limits['monthly_generations']:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": f"Monthly generation limit exceeded ({tier_limits['monthly_generations']})",
                "limit": tier_limits['monthly_generations'],
                "used": profile['monthly_generations'],
                "reset_date": profile['last_reset_date']
            }
        )

    # Check API rate limiting (requests per minute)
    rate_limit_key = f"rate_limit:{user['id']}:{datetime.now().minute}"
    current_requests = redis_client.get(rate_limit_key)

    requests_per_minute = 60 if profile['tier'] == UserTier.ENTERPRISE else 30

    if current_requests and int(current_requests) >= requests_per_minute:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "api_rate_limit_exceeded",
                "message": f"API rate limit exceeded ({requests_per_minute} requests per minute)",
                "retry_after": 60
            }
        )

    # Increment rate limit counter
    redis_client.incr(rate_limit_key)
    redis_client.expire(rate_limit_key, 60)

    return user

def require_tier(required_tier: str):
    """Decorator to require specific user tier"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user = Depends(get_current_user), **kwargs):
            tier_hierarchy = [UserTier.FREE, UserTier.PRO, UserTier.ENTERPRISE]
            user_tier_level = tier_hierarchy.index(current_user['tier'])
            required_tier_level = tier_hierarchy.index(required_tier)

            if user_tier_level < required_tier_level:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "insufficient_tier",
                        "message": f"This feature requires {required_tier} tier or higher",
                        "current_tier": current_user['tier'],
                        "required_tier": required_tier
                    }
                )

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

async def check_database_connection():
    """Check if database is accessible"""
    try:
        result = supabase.table('user_profiles').select('id').limit(1).execute()
        return True
    except Exception:
        return False

async def check_supabase_connection():
    """Check if Supabase is accessible"""
    try:
        # Try to get current timestamp
        result = supabase.rpc('now').execute()
        return True
    except Exception:
        return False
```

### **Enhanced Configuration Management**

```python
# sushi-kitchen-api/app/services/configuration_service.py
from typing import List, Dict, Optional
import hashlib
import json
from datetime import datetime

class ConfigurationService:
    def __init__(self, supabase_client, orchestrator):
        self.supabase = supabase_client
        self.orchestrator = orchestrator

    async def save_configuration(
        self,
        user_id: str,
        name: str,
        description: Optional[str],
        selection_type: str,
        selection_id: str,
        privacy_profile: str,
        include_optional: bool,
        config_data: Dict,
        is_public: bool = False,
        tags: List[str] = None
    ) -> str:
        """Save a configuration and return its ID"""

        config_yaml = yaml.dump(config_data)
        config_hash = hashlib.sha256(config_yaml.encode()).hexdigest()

        # Check if identical configuration already exists
        existing = self.supabase.table('saved_configurations')\
            .select('id')\
            .eq('user_id', user_id)\
            .eq('config_hash', config_hash)\
            .execute()

        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="Identical configuration already saved"
            )

        # Check user's saved configuration limits
        user_configs_count = len(
            self.supabase.table('saved_configurations')\
            .select('id')\
            .eq('user_id', user_id)\
            .execute().data
        )

        # Get user profile to check limits
        profile = self.supabase.table('user_profiles')\
            .select('tier')\
            .eq('id', user_id)\
            .single()\
            .execute()

        tier_limits = TIER_LIMITS[profile.data['tier']]
        if user_configs_count >= tier_limits['saved_configurations']:
            raise HTTPException(
                status_code=403,
                detail=f"Saved configuration limit exceeded ({tier_limits['saved_configurations']})"
            )

        # Save configuration
        config_record = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'selection_type': selection_type,
            'selection_id': selection_id,
            'privacy_profile': privacy_profile,
            'include_optional': include_optional,
            'generated_config': config_data,
            'config_hash': config_hash,
            'is_public': is_public,
            'tags': tags or []
        }

        result = self.supabase.table('saved_configurations')\
            .insert(config_record)\
            .execute()

        return result.data[0]['id']

    async def get_public_configurations(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = 'created_at'
    ) -> Dict:
        """Get public configurations with filtering and pagination"""

        query = self.supabase.table('saved_configurations')\
            .select('''
                *,
                user_profiles!inner(full_name, organization)
            ''')\
            .eq('is_public', True)

        # Apply search filter
        if search:
            query = query.or_(
                f"name.ilike.%{search}%,"
                f"description.ilike.%{search}%,"
                f"tags.cs.{{{search}}}"
            )

        # Apply tag filter
        if tags:
            for tag in tags:
                query = query.contains('tags', [tag])

        # Apply sorting
        sort_column = sort_by
        if sort_by == 'popularity':
            sort_column = 'download_count'
        elif sort_by == 'likes':
            sort_column = 'like_count'

        # Get total count
        count_result = query.execute()
        total_count = len(count_result.data)

        # Get paginated results
        offset = (page - 1) * limit
        configurations = query\
            .order(sort_column, desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()

        return {
            'configurations': configurations.data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }

    async def fork_configuration(
        self,
        user_id: str,
        source_config_id: str,
        new_name: str
    ) -> str:
        """Fork a public configuration to user's account"""

        # Get source configuration
        source = self.supabase.table('saved_configurations')\
            .select('*')\
            .eq('id', source_config_id)\
            .eq('is_public', True)\
            .single()\
            .execute()

        if not source.data:
            raise HTTPException(status_code=404, detail="Configuration not found")

        # Create forked configuration
        forked_config = source.data.copy()
        forked_config.update({
            'id': None,  # Will be auto-generated
            'user_id': user_id,
            'name': new_name,
            'is_public': False,
            'parent_config_id': source_config_id,
            'download_count': 0,
            'like_count': 0,
            'fork_count': 0
        })

        result = self.supabase.table('saved_configurations')\
            .insert(forked_config)\
            .execute()

        # Increment fork count on source
        self.supabase.table('saved_configurations')\
            .update({'fork_count': source.data['fork_count'] + 1})\
            .eq('id', source_config_id)\
            .execute()

        return result.data[0]['id']
```

### **Pre-Built Configuration System**

```python
# sushi-kitchen-api/app/services/prebuilt_service.py - Complete implementation
import json
import asyncio
from pathlib import Path
from typing import Dict, Optional, List
import aiofiles
from datetime import datetime, timedelta

class PreBuiltConfigurationService:
    def __init__(self, supabase_client, orchestrator):
        self.supabase = supabase_client
        self.orchestrator = orchestrator
        self.prebuilt_dir = Path('/app/prebuilt')
        self.cache = {}
        self.cache_ttl = {}

    async def get_or_generate_configuration(
        self,
        selection_type: str,
        selection_id: str,
        privacy_profile: str,
        include_optional: bool = False
    ) -> tuple[Dict, str]:  # Returns (config, source)
        """Get configuration with intelligent fallback strategy"""

        # Try pre-built first
        prebuilt_config = await self._get_prebuilt_configuration(
            selection_type, selection_id, privacy_profile, include_optional
        )

        if prebuilt_config:
            return prebuilt_config, "prebuilt"

        # Try cache
        cached_config = await self._get_cached_configuration(
            selection_type, selection_id, privacy_profile, include_optional
        )

        if cached_config:
            return cached_config, "cached"

        # Generate fresh configuration
        fresh_config = await self.orchestrator.generate_complete_stack(
            selection_type=selection_type,
            selection_id=selection_id,
            profile=privacy_profile,
            include_optional=include_optional
        )

        # Cache the result
        await self._cache_configuration(
            selection_type, selection_id, privacy_profile,
            include_optional, fresh_config
        )

        # Consider pre-building if popular
        await self._consider_prebuild(
            selection_type, selection_id, privacy_profile, include_optional
        )

        return fresh_config, "generated"

    async def _get_prebuilt_configuration(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool
    ) -> Optional[Dict]:
        """Get pre-built configuration from filesystem"""

        filename = self._get_prebuilt_filename(
            selection_type, selection_id, privacy_profile, include_optional
        )

        if not filename.exists():
            return None

        try:
            async with aiofiles.open(filename, 'r') as f:
                content = await f.read()
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    async def _get_cached_configuration(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool
    ) -> Optional[Dict]:
        """Get configuration from in-memory cache"""

        cache_key = self._generate_cache_key(
            selection_type, selection_id, privacy_profile, include_optional
        )

        # Check if cached and not expired
        if cache_key in self.cache:
            if cache_key in self.cache_ttl:
                if datetime.now() < self.cache_ttl[cache_key]:
                    return self.cache[cache_key]
                else:
                    # Expired, remove from cache
                    del self.cache[cache_key]
                    del self.cache_ttl[cache_key]

        return None

    async def _cache_configuration(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool, config: Dict
    ):
        """Cache configuration in memory"""

        cache_key = self._generate_cache_key(
            selection_type, selection_id, privacy_profile, include_optional
        )

        self.cache[cache_key] = config
        self.cache_ttl[cache_key] = datetime.now() + timedelta(hours=1)

    async def _consider_prebuild(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool
    ):
        """Determine if configuration should be pre-built"""

        # Update popularity tracking
        popularity_record = {
            'selection_type': selection_type,
            'selection_id': selection_id,
            'privacy_profile': privacy_profile,
            'include_optional': include_optional,
            'generation_count': 1,
            'last_generated': datetime.now().isoformat()
        }

        self.supabase.table('configuration_popularity')\
            .upsert(popularity_record,
                   on_conflict='selection_type,selection_id,privacy_profile,include_optional')\
            .execute()

        # Check if should be pre-built (threshold: 10 generations)
        result = self.supabase.table('configuration_popularity')\
            .select('generation_count')\
            .eq('selection_type', selection_type)\
            .eq('selection_id', selection_id)\
            .eq('privacy_profile', privacy_profile)\
            .eq('include_optional', include_optional)\
            .single()\
            .execute()

        if result.data and result.data['generation_count'] >= 10:
            # Schedule for pre-building (would trigger CI/CD job in production)
            await self._schedule_prebuild(
                selection_type, selection_id, privacy_profile, include_optional
            )

    async def get_popular_configurations(self, limit: int = 50) -> List[Dict]:
        """Get most popular configurations for pre-building"""

        result = self.supabase.table('configuration_popularity')\
            .select('*')\
            .order('generation_count', desc=True)\
            .order('last_generated', desc=True)\
            .limit(limit)\
            .execute()

        return result.data

    def _generate_cache_key(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool
    ) -> str:
        """Generate consistent cache key"""
        key_data = f"{selection_type}:{selection_id}:{privacy_profile}:{include_optional}"
        return hashlib.sha256(key_data.encode()).hexdigest()

    def _get_prebuilt_filename(
        self, selection_type: str, selection_id: str,
        privacy_profile: str, include_optional: bool
    ) -> Path:
        """Get filename for pre-built configuration"""

        # Sanitize components for filesystem
        clean_type = selection_type.replace('.', '_').replace('-', '_')
        clean_id = selection_id.replace('.', '_').replace('-', '_')
        clean_profile = privacy_profile.replace('.', '_').replace('-', '_')
        optional_suffix = '_optional' if include_optional else ''

        filename = f"{clean_type}_{clean_id}_{clean_profile}{optional_suffix}.json"
        return self.prebuilt_dir / filename

    async def health_check(self) -> bool:
        """Check if pre-built service is healthy"""
        try:
            # Check if prebuilt directory exists
            if not self.prebuilt_dir.exists():
                return False

            # Check if we have any pre-built configurations
            prebuilt_files = list(self.prebuilt_dir.glob('*.json'))
            if len(prebuilt_files) == 0:
                return False

            # Try to load a random pre-built file
            test_file = prebuilt_files[0]
            async with aiofiles.open(test_file, 'r') as f:
                content = await f.read()
                json.loads(content)  # Verify it's valid JSON

            return True

        except Exception:
            return False
```

## 🚀 Performance Requirements

### **Response Time Targets**
- Authentication: < 200ms
- Pre-built configuration serving: < 500ms
- Custom configuration generation: < 10 seconds
- Public configuration browsing: < 1 second
- User dashboard loading: < 2 seconds

### **Scalability Requirements**
- Support 1000+ concurrent users
- Handle 10,000+ configurations in database
- Support 100+ pre-built configurations
- Cache hit rate > 80% for popular configurations

### **Reliability Requirements**
- 99.9% uptime SLA
- Automatic failover for database connections
- Graceful degradation when external services unavailable
- Data backup and recovery procedures

This technical specification provides the complete implementation details needed to build the remaining 20% of functionality and achieve the target user experience.