import os

class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "url_shortener")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

settings = Settings()
