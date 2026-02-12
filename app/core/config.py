from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "academia-del-barrio"
    environment: str = "local"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+psycopg://postgres:dPUyBFH0105@localhost:5432/academia_del_barrio"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
