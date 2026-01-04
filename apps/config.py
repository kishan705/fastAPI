
#config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# This finds the absolute path to the folder where THIS file (config.py) is located
# Result: /Users/kishanamaliya/Desktop/fastAPI/apps/
APP_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        # We join the folder path with the filename to get the exact location
        env_file=os.path.join(APP_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()