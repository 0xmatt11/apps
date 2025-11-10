from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from .chatgpt_client import ChatGPTClient
from .config import AppConfig
from .idea_store import IdeaStore
from .twitter_client import TwitterClient

logger = logging.getLogger(__name__)


class TweetScheduler:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._idea_store = IdeaStore(config.ideas_path)
        self._chatgpt = ChatGPTClient(
            api_key=config.openai.api_key,
            chat_model=config.openai.chat_model,
            image_model=config.openai.image_model,
        )
        self._twitter = TwitterClient(
            consumer_key=config.twitter.consumer_key,
            consumer_secret=config.twitter.consumer_secret,
            access_token=config.twitter.access_token,
            access_token_secret=config.twitter.access_token_secret,
        )

    async def run_once(self) -> None:
        idea = self._idea_store.next_idea()
        logger.info("Selected idea: %s", idea.title)
        content = self._chatgpt.generate_content(idea)
        logger.info("Generated tweet text (%d chars)", len(content.tweet_text))
        image_bytes = self._chatgpt.generate_image(content.image_prompt)
        logger.info("Generated image prompt: %s", content.image_prompt)
        self._twitter.post_tweet_with_image(content.tweet_text, image_bytes)
        logger.info("Tweet posted at %s", datetime.utcnow().isoformat())

    async def run_forever(self) -> None:
        interval_seconds = int(self._config.scheduler.interval.total_seconds())
        while True:
            await self.run_once()
            logger.info("Sleeping for %s seconds", interval_seconds)
            await asyncio.sleep(interval_seconds)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


async def run(once: bool = False) -> None:
    configure_logging()
    config = AppConfig.load()
    scheduler = TweetScheduler(config)
    if once:
        await scheduler.run_once()
    else:
        await scheduler.run_forever()
