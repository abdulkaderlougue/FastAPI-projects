from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # load from .env file
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()