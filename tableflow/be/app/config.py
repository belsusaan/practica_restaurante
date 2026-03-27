from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    token_expire_minutes: int = 60
    algorithm: str = "HS256"
    kitchen_grpc_host: str = "localhost"
    kitchen_grpc_port: int = 50051


settings = Settings()
