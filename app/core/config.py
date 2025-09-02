
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    NEO4J_URL: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    NATS_URL: str = "nats://nats:4222"

    class Config:
        env_file = ".env"

settings = Settings()
