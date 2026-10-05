import os

class Settings:
    # Docker-compose içindeki nginx servisine istek atacak
    API_URL = os.getenv("API_URL", "http://nginx:80")

settings = Settings()