from __future__ import annotations

import re
from pathlib import Path


def main() -> None:
    tex = Path("paper/main.tex").read_text(encoding="utf-8")
    bib = Path("paper/references.bib").read_text(encoding="utf-8")
    cited = set()
    for match in re.findall(r"\\cite\{([^}]+)\}", tex):
        cited.update(part.strip() for part in match.split(","))
    available = set(re.findall(r"@\w+\{([^,]+),", bib))
    missing = sorted(cited - available)
    unused = sorted(available - cited)
    if missing:
        raise SystemExit("missing bibliography keys: " + ", ".join(missing))
    print(f"citation check passed: {len(cited)} cited, {len(unused)} unused")


if __name__ == "__main__":
    main()
