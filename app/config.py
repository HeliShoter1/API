from pydantic import BaseSettings

class Setting(BaseSettings):
    dataBase_Hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorimthm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'

setting = Setting()