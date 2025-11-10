# Automated ChatGPT ➜ X/Twitter Poster

This repository contains a small Python tool that coordinates ChatGPT (via the OpenAI API) and X/Twitter to publish an AI-generated tweet every two hours. The workflow is:

1. Rotate through a configurable list of ideas.
2. Ask ChatGPT to turn the idea into tweet copy and an art prompt.
3. Generate an accompanying illustration.
4. Publish the tweet + image on X/Twitter.

## Project layout

```
auto_tweet_bot/
├── __init__.py
├── __main__.py        # CLI entry point
├── chatgpt_client.py  # ChatGPT + image generation helpers
├── config.py          # Environment-driven configuration objects
├── idea_store.py      # Persistent list of recurring ideas
├── scheduler.py       # Two-hour job loop
└── twitter_client.py  # Posting logic using Tweepy
ideas.json             # Example idea list (rotating)
requirements.txt       # Runtime dependencies
```

## Prerequisites

* Python 3.10+
* OpenAI API access (for both text + image generation)
* X/Twitter API credentials with write permissions

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Export the required credentials before running the tool:

```bash
export OPENAI_API_KEY="sk-..."
export TWITTER_CONSUMER_KEY="..."
export TWITTER_CONSUMER_SECRET="..."
export TWITTER_ACCESS_TOKEN="..."
export TWITTER_ACCESS_TOKEN_SECRET="..."
```

You can also override the ideas file location by setting `IDEAS_FILE` to a custom path.

### Managing ideas

`ideas.json` contains an array of idea objects and tracks which one was used last. Update the list with your recurring themes; the scheduler will loop over them sequentially.

Example snippet:

```json
{
  "ideas": [
    {
      "title": "Sunrise mindfulness",
      "description": "Share a gentle mindfulness ritual inspired by sunrise colors."
    }
  ],
  "last_index": -1
}
```

## Running the scheduler

Run continuously (every two hours):

```bash
python -m auto_tweet_bot
```

Run a single cycle (useful for testing):

```bash
python -m auto_tweet_bot --once
```

The script logs progress to stdout (idea selection, prompt generation, tweet status). Combine it with a process manager such as `systemd`, `supervisord`, or a container scheduler to keep it alive in production.

## Notes & safety

* The script posts immediately after generating content—review outputs during initial runs.
* OpenAI image generation costs can add up; monitor usage and consider lowering the frequency for testing.
* Handle your API keys securely and never commit them to version control.
