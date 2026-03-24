#!/usr/bin/env python3
import json
import sys


def main():
    data = json.loads(sys.stdin.read() or "{}")
    mode = data.get("product_source_mode")
    normalized = {"mode": mode}
    if mode == "upload":
        normalized["upload_status"] = data.get("product_upload_status")
    elif mode == "ds":
        normalized["criteria"] = data.get("product_ds_criteria") or {}
    elif mode == "none":
        normalized["site_type"] = data.get("no_product_site_type")
    print(json.dumps({"ok": True, "normalized": normalized}, ensure_ascii=False))


if __name__ == "__main__":
    main()
