from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Social Rankings API"
    app_env: str = "local"
    app_port: int = 8000
    log_level: str = "INFO"
    run_migrations_on_startup: bool = True
    database_url: str = "sqlite:///./social_rankings.db"
    api_key: str = "767ge4j63d"
    aws_region: str = "us-east-1"
    aws_secrets_manager_db_secret_arn: str | None = None
    aws_secrets_manager_api_key_secret_arn: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
