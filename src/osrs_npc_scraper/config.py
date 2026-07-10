from pydantic import (
    computed_field,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurable settings for project"""

    model_config = SettingsConfigDict(env_prefix="APP_")

    # scraper settings
    base_wiki_url: str = Field(
        default="https://oldschool.runescape.wiki", description="Wiki base URL"
    )
    npc_wiki_path: str = Field(
        default="/w/Category:Non-player_characters",
        description="URL path for NPC wiki pages table",
    )
    request_timeout: int = Field(
        default=10,
        description="How many seconds to wait before timing out on a request",
    )
    request_delay: int = Field(
        default=3, description="How many seconds to wait between each request"
    )
    max_retries: int = Field(
        default=3, description="How many times to re-attempt request upon failure"
    )

    @computed_field
    @property
    def npc_wiki_url(self) -> str:
        return self.base_wiki_url + self.npc_wiki_path
