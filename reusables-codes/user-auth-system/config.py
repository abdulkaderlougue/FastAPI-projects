from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "User Authentication System"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # get values from .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()