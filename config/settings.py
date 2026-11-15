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

    # device index (int) or name + audio API (str), e.g. "Realtek MME"; None = system default
    mic_device: Annotated[int | str | None, Field(union_mode="left_to_right")] = None


settings = Settings()
