from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    redis_url: str
    OPENAI_API_KEY:str

    class Config:
        env_file = ".env"
        extra = "ignore"  # This will reject any unknown fields
settings = Settings()
