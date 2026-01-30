from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root@localhost/alfiyah_db"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()
