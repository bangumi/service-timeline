import uuid
from typing import Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)

    # 微服务相关的环境变量
    node_id: str = Field(str(uuid.uuid4()), env="NODE_ID")
    etcd_prefix: str = Field("/chii/services", env="ETCD_PREFIX")
    etcd_addr: Optional[AnyHttpUrl] = Field(env="ETCD_ADDR")
    external_address: str = Field("127.0.0.1", env="EXTERNAL_ADDRESS")

    MYSQL_HOST: str = Field(env="MYSQL_HOST", default="127.0.0.1")
    MYSQL_PORT: int = Field(env="MYSQL_PORT", default=3306)
    MYSQL_USER: str = Field(env="MYSQL_USER", default="user")
    MYSQL_PASS: str = Field(env="MYSQL_PASS", default="password")
    MYSQL_DB: str = Field(env="MYSQL_DB", default="bangumi")

    COMMIT_REF: str = Field(env="COMMIT_REF", default="dev")
    grpc_port: int = Field(env="GRPC_PORT", default=5000)
    grpc_max_workers: int = Field(env="GRPC_MAX_WORKERS", default=10)

    SLOW_SQL_MS: int = Field(env="SLOW_SQL_MS", default=0)

    @property
    def MYSQL_SYNC_DSN(self) -> str:
        return "mysql+pymysql://{}:{}@{}:{}/{}".format(
            self.MYSQL_USER,
            self.MYSQL_PASS,
            self.MYSQL_HOST,
            self.MYSQL_PORT,
            self.MYSQL_DB,
        )


load_dotenv()
config = Settings()

if __name__ == "__main__":
    print(config.dict())
