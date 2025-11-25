from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# Project-wide settings
class Settings(BaseSettings):
    database_url: str

    # Tell Pydantic to read variables from a .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings() 
