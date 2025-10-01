"""
Configuration settings for SavorMe Backend
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "SavorMe Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API Keys
    EDAMAM_APP_ID: Optional[str] = Field(None, env="EDAMAM_APP_ID")
    EDAMAM_APP_KEY: Optional[str] = Field(None, env="EDAMAM_APP_KEY")
    USDA_API_KEY: Optional[str] = Field(None, env="USDA_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = Field(None, env="OPENROUTER_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(None, env="HUGGINGFACE_API_KEY")
    
    # Canva API (for design generation)
    CANVA_CLIENT_ID: Optional[str] = Field(None, env="CANVA_CLIENT_ID")
    CANVA_CLIENT_SECRET: Optional[str] = Field(None, env="CANVA_CLIENT_SECRET")
    CANVA_ACCESS_TOKEN: Optional[str] = Field(None, env="CANVA_ACCESS_TOKEN")
    
    # Database
    DATABASE_URL: str = Field("sqlite:///./savorme.db", env="DATABASE_URL")
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # API Configuration
    EDAMAM_BASE_URL: str = "https://api.edamam.com/api/recipes/v2"
    USDA_BASE_URL: str = "https://api.nal.usda.gov/fdc/v1"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    HUGGINGFACE_BASE_URL: str = "https://api-inference.huggingface.co/models"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

