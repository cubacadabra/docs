#!/usr/bin/env python3
"""Check the canonical documentation corpus without third-party packages."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = sorted(ROOT.rglob("*.md"))
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RETIRED_LINK_RE = re.compile(
    r"(?:^|/)(?:backend|developer|ios_app|rust|studio|tools|web)/docs(?:/|$)"
)
ALLOWED_MATURITY = {"Preview", "Experimental", "Stable"}


def check_relative_links(errors: list[str]) -> None:
    for page in MARKDOWN:
        for target in LINK_RE.findall(page.read_text()):
            target = target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "tel:")):
                continue
            if RETIRED_LINK_RE.search(target):
                errors.append(f"{page.relative_to(ROOT)} links to retired docs path {target}")
                continue
            if not (page.parent / target).resolve().exists():
                errors.append(f"{page.relative_to(ROOT)} has broken relative link {target}")


def check_ledger_destinations(errors: list[str]) -> None:
    ledger = ROOT / "sources.md"
    for line in ledger.read_text().splitlines():
        if not line.startswith("|"):
            continue
        for token in re.findall(r"`([^`]+\.md)`", line):
            if "/docs/" in token or token.startswith("docs/"):
                continue
            path = (ROOT / token).resolve()
            if not path.exists():
                errors.append(f"sources.md names missing canonical destination {token}")


def check_contract_status(errors: list[str]) -> None:
    pages = [p for p in (ROOT / "contracts").glob("*.md") if p.name != "README.md"]
    pages += [p for p in (ROOT / "contracts" / "sdk").glob("*.md") if p.name != "README.md"]
    for page in pages:
        text = page.read_text()
        if "**Status:** Current contract" not in text:
            errors.append(f"{page.relative_to(ROOT)} lacks Status: Current contract")
        match = re.search(r"\*\*Maturity:\*\* ([^\n]+)", text)
        if not match or match.group(1).strip() not in ALLOWED_MATURITY:
            errors.append(f"{page.relative_to(ROOT)} lacks an allowed maturity")


def main() -> int:
    errors: list[str] = []
    check_relative_links(errors)
    check_ledger_destinations(errors)
    check_contract_status(errors)
    if errors:
        print("Documentation checks failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Documentation checks passed ({len(MARKDOWN)} Markdown files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
