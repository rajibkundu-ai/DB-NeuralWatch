from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "DB NeuralWatch"
    admin_username: str = Field(..., description="Username for the built-in admin account")
    admin_password: str = Field(..., description="Password for the built-in admin account")
    secret_key: str = Field(..., description="Secret key for JWT signing")
    access_token_expire_minutes: int = Field(60, description="Access token lifetime in minutes")

    sqlserver_connection_string: str = Field("", description="ODBC connection string for SQL Server")
    metrics_poll_interval: int = Field(30, description="Seconds between metric collection cycles")

    alert_cpu_threshold: float = Field(85.0)
    alert_memory_threshold: float = Field(85.0)
    alert_disk_io_threshold: float = Field(80.0)

    retention_hours: int = Field(24 * 14, description="Number of hours of metrics to retain in SQLite")

    backend_api_url: str = Field(
        "http://localhost:8000/api",
        description="Public base URL for the backend API (including the base path)",
    )
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Comma-separated list of origins allowed to access the API",
    )

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value: str | list[str]):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
