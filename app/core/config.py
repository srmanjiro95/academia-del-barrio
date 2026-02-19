from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "academia-del-barrio"
    environment: str = "local"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/academia_del_barrio"

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = False
    smtp_from_email: str = "no-reply@academiadelbarrio.local"

    public_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
