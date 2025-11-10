from __future__ import annotations

import base64
import json
from dataclasses import dataclass

from openai import OpenAI

from .idea_store import Idea


@dataclass
class GeneratedContent:
    tweet_text: str
    image_prompt: str


class ChatGPTClient:
    """Wraps the OpenAI API to derive tweet copy and art prompts."""

    def __init__(self, api_key: str, chat_model: str, image_model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._chat_model = chat_model
        self._image_model = image_model

    def generate_content(self, idea: Idea) -> GeneratedContent:
        system_prompt = (
            "You are an assistant that prepares engaging tweets and illustration prompts "
            "for an automated social media account."
        )
        user_prompt = (
            "Using the following idea, craft an engaging tweet and a concise image generation "
            "prompt. Respond strictly as JSON with the keys 'tweet_text' and 'image_prompt'.\n\n"
            f"{idea.to_prompt_fragment()}\n"
            "Tweet requirements:\n"
            "- Maximum of 250 characters.\n"
            "- Include relevant hashtags.\n"
            "- Be friendly and inspirational.\n\n"
            "Image prompt requirements:\n"
            "- Be vivid, visually descriptive, and mention the desired artistic style.\n"
            "- Avoid referencing text or typography.\n"
        )
        response = self._client.responses.create(
            model=self._chat_model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        payload = json.loads(response.output_text)
        return GeneratedContent(
            tweet_text=payload["tweet_text"].strip(),
            image_prompt=payload["image_prompt"].strip(),
        )

    def generate_image(self, prompt: str, *, size: str = "1024x1024") -> bytes:
        response = self._client.images.generate(
            model=self._image_model,
            prompt=prompt,
            size=size,
            response_format="b64_json",
        )
        image_data = response.data[0].b64_json
        return base64.b64decode(image_data)


__all__ = ["ChatGPTClient", "GeneratedContent"]
