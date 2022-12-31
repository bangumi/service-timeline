from dotenv import load_dotenv
from pydantic import Field, BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)

    MYSQL_HOST: str = Field(env="MYSQL_HOST", default="127.0.0.1")
    MYSQL_PORT: int = Field(env="MYSQL_PORT", default=3306)
    MYSQL_USER: str = Field(env="MYSQL_USER", default="user")
    MYSQL_PASS: str = Field(env="MYSQL_PASS", default="password")
    MYSQL_DB: str = Field(env="MYSQL_DB", default="bangumi")

    COMMIT_REF: str = Field(env="COMMIT_REF", default="dev")
    grpc_port: int = Field(env="GRPC_PORT", default=5000)

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
