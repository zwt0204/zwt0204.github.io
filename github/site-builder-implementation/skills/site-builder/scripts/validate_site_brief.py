#!/usr/bin/env python3
import json
import sys


def main():
    data = json.loads(sys.stdin.read() or "{}")
    errors = []
    if not data.get("industry"):
        errors.append("industry is required")
    if not data.get("language"):
        errors.append("language is missing")
    if not data.get("style"):
        errors.append("style is missing")
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False))


if __name__ == "__main__":
    main()
