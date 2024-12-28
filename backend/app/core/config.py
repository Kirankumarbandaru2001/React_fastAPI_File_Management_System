from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    AWS_S3_BUCKET: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
