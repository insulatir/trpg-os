from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CAMPAIGN_PATH: str = "../campaigns/default"
    XLSX_FILE: str = "TRPG_Campaign_State.xlsx"
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.7
    MAX_RECENT_EVENTS: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
