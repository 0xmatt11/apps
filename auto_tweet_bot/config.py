from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timedelta


class MissingEnvironmentVariableError(RuntimeError):
    """Raised when a required environment variable is missing."""


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise MissingEnvironmentVariableError(
        f"The environment variable {name!r} must be set for the Twitter bot to run."
    )


@dataclass(frozen=True)
class OpenAIConfig:
    api_key: str
    chat_model: str = "gpt-4.1-mini"
    image_model: str = "gpt-image-1"

    @classmethod
    def load_from_env(cls) -> "OpenAIConfig":
        return cls(api_key=_require_env("OPENAI_API_KEY"))


@dataclass(frozen=True)
class TwitterConfig:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

    @classmethod
    def load_from_env(cls) -> "TwitterConfig":
        return cls(
            consumer_key=_require_env("TWITTER_CONSUMER_KEY"),
            consumer_secret=_require_env("TWITTER_CONSUMER_SECRET"),
            access_token=_require_env("TWITTER_ACCESS_TOKEN"),
            access_token_secret=_require_env("TWITTER_ACCESS_TOKEN_SECRET"),
        )


@dataclass(frozen=True)
class SchedulerConfig:
    interval: timedelta

    @classmethod
    def every_two_hours(cls) -> "SchedulerConfig":
        return cls(interval=timedelta(hours=2))


@dataclass(frozen=True)
class AppConfig:
    openai: OpenAIConfig
    twitter: TwitterConfig
    scheduler: SchedulerConfig
    ideas_path: str

    @classmethod
    def load(cls, ideas_path: str | None = None) -> "AppConfig":
        return cls(
            openai=OpenAIConfig.load_from_env(),
            twitter=TwitterConfig.load_from_env(),
            scheduler=SchedulerConfig.every_two_hours(),
            ideas_path=ideas_path or os.getenv("IDEAS_FILE", "ideas.json"),
        )
