from pathlib import Path
from typing  import Annotated

from pydantic          import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env in the project root – found regardless of the current working directory
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Environment-specific settings: env variables > .env > defaults below."""

    model_config = SettingsConfigDict(
        env_file         = ENV_FILE,
        extra            = "ignore",   # ignore unrelated entries in .env
        env_ignore_empty = True,       # MIC_DEVICE= in .env means "use default"
    )

    mic_device:     str | None                          = None
    wake_threshold: Annotated[float, Field(ge=0, le=1)] = 0.5
    wake_word:      str                                 = "hey_jarvis"


settings = Settings()
