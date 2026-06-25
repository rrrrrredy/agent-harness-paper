from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.providers import PROVIDERS, has_provider_key, provider_env_var


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=[*PROVIDERS.keys(), "all"], default="all")
    args = parser.parse_args()

    providers = list(PROVIDERS) if args.provider == "all" else [args.provider]
    missing = [provider_env_var(provider) for provider in providers if not has_provider_key(provider)]
    if missing:
        raise SystemExit("missing provider credential environment variables: " + ", ".join(missing))
    print("provider credential preflight passed for: " + ", ".join(providers))


if __name__ == "__main__":
    main()
