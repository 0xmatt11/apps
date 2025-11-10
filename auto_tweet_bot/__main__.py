from __future__ import annotations

import argparse
import asyncio

from .scheduler import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated ChatGPT-powered Twitter bot")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the workflow only once instead of continuously",
    )
    args = parser.parse_args()
    asyncio.run(run(once=args.once))


if __name__ == "__main__":
    main()
