#!/usr/bin/env python3
import json
import sys

STYLE_MAP = {
    "jewelry": ["luxury minimal", "premium editorial", "soft luxury", "visual storytelling"],
    "beauty": ["elegant clean", "premium editorial", "soft luxury"],
    "electronics": ["modern tech", "minimal dark", "precision clean"],
    "home decor": ["warm minimal", "editorial calm", "premium lifestyle"],
}


def main():
    industry = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
    styles = STYLE_MAP.get(industry, ["modern minimal", "premium clean", "editorial light"])
    print(json.dumps({"ok": True, "industry": industry, "style_suggestions": styles}, ensure_ascii=False))


if __name__ == "__main__":
    main()
