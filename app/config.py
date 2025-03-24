from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EnvironmentVariables(BaseSettings):
    AI_NAME: str
    TG_BOT_API_TOKEN: str
    TG_WEBHOOK_TOKEN: str

    OPENAI_API_KEY: str

    DATABASE_URL: str
    """
    docker run -d \
      --name chatbot \
      -e POSTGRES_USER=postgres \
      -e POSTGRES_PASSWORD=postgres \
      -e POSTGRES_DB=chatbot \
      -p 5431:5432 \
      docker.io/postgres
    """

    model_config = SettingsConfigDict(env_file=".env")


env = EnvironmentVariables()
