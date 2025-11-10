from __future__ import annotations

import tempfile
from pathlib import Path

import tweepy


class TwitterClient:
    """Handles authentication and posting tweets with images."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        self._client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        self._api_v1 = tweepy.API(auth)

    def post_tweet_with_image(self, text: str, image_bytes: bytes) -> None:
        if not text.strip():
            raise ValueError("Tweet text must not be empty")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_file.write(image_bytes)
            tmp_file.flush()
            temp_path = Path(tmp_file.name)
        try:
            media = self._api_v1.media_upload(filename=str(temp_path))
            self._client.create_tweet(text=text, media_ids=[media.media_id])
        finally:
            temp_path.unlink(missing_ok=True)


__all__ = ["TwitterClient"]
