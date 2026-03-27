import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_super_secreta")
    secret_key: str = os.getenv("SECRET_KEY", "tu_clave_super_secreta")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    algorithm: str = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    access_token_expire_minutes: int = 30

    DB_USER: str = os.getenv("MYSQL_USER", "tableuser")
    DB_PASS: str = os.getenv("MYSQL_PASSWORD", "tablepass")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_NAME: str = os.getenv("MYSQL_DATABASE", "tableflow")

    KITCHEN_GRPC_HOST: str = os.getenv("KITCHEN_GRPC_HOST", "kitchen")
    kitchen_grpc_host: str = os.getenv("KITCHEN_GRPC_HOST", "kitchen")

    KITCHEN_GRPC_PORT: int = int(os.getenv("KITCHEN_GRPC_PORT", "50051"))
    kitchen_grpc_port: int = int(os.getenv("KITCHEN_GRPC_PORT", "50051"))

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"


settings = Settings()
