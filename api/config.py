import os

class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "url_shortener")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")

    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

settings = Settings()

