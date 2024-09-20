import os
import uuid
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings, validate_default=True):
    debug: bool = os.environ.get("DEBUG", False)  # type: ignore

    # 微服务相关的环境变量
    node_id: str = os.getenv("NODE_ID") or str(uuid.uuid4())  # type: ignore
    etcd_prefix: str = os.getenv("ETCD_PREFIX") or "/chii/services"  # type: ignore
    etcd_addr: Optional[AnyHttpUrl] = os.getenv("ETCD_ADDR") or None  # type: ignore
    external_address: str = os.getenv("EXTERNAL_ADDRESS") or "127.0.0.1"  # type: ignore

    MYSQL_HOST: str = os.getenv("MYSQL_HOST") or "127.0.0.1"  # type: ignore
    MYSQL_PORT: int = os.getenv("MYSQL_PORT") or 3306  # type: ignore
    MYSQL_USER: str = os.getenv("MYSQL_USER") or "user"  # type: ignore
    MYSQL_PASS: str = os.getenv("MYSQL_PASS") or "password"  # type: ignore
    MYSQL_DB: str = os.getenv("MYSQL_DB") or "bangumi"  # type: ignore

    COMMIT_REF: str = os.getenv("COMMIT_REF") or "dev"  # type: ignore
    grpc_port: int = os.getenv("GRPC_PORT") or 5000  # type: ignore
    grpc_max_workers: int = os.getenv("GRPC_MAX_WORKERS") or 10  # type: ignore

    SLOW_SQL_MS: int = os.getenv("SLOW_SQL_MS") or 0  # type: ignore

    @property
    def MYSQL_SYNC_DSN(self) -> str:
        return "mysql+pymysql://{}:{}@{}:{}/{}".format(
            self.MYSQL_USER,
            self.MYSQL_PASS,
            self.MYSQL_HOST,
            self.MYSQL_PORT,
            self.MYSQL_DB,
        )


config = Settings()

if __name__ == "__main__":
    print(config.model_dump())
