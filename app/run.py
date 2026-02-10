from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .model_client import build_model_client
from .pipeline import IntakePipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline legal intake pipeline demo")
    parser.add_argument("--text", help="Raw user intake text", default="")
    parser.add_argument("--input-file", help="Path to text file", default="")
    parser.add_argument(
        "--provider",
        default=os.getenv("MODEL_PROVIDER", "mock"),
        choices=["mock", "groq", "ollama"],
        help="Model provider",
    )

    args = parser.parse_args()

    if args.input_file:
        user_text = Path(args.input_file).read_text(encoding="utf-8")
    elif args.text:
        user_text = args.text
    else:
        user_text = (
            "I need a prenup in CA. I have about 250000 in separate assets, "
            "no children, wedding is June 10, 2027."
        )

    client = build_model_client(args.provider)
    pipeline = IntakePipeline(client, provider_name=args.provider)
    result = pipeline.run(user_text=user_text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
