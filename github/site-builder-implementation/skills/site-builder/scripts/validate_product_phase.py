#!/usr/bin/env python3
import json
import sys


def main():
    data = json.loads(sys.stdin.read() or "{}")
    mode = data.get("product_source_mode")
    errors = []
    if not mode:
        errors.append("product_source_mode is required")
    elif mode == "upload":
        status = data.get("product_upload_status")
        if status not in {"received", "confirmed"}:
            errors.append("upload products not ready")
    elif mode == "ds":
        ds = data.get("product_ds_criteria") or {}
        if not ds.get("category"):
            errors.append("ds category is required")
        if not ds.get("market"):
            errors.append("ds market is required")
        if not ds.get("price_range"):
            errors.append("ds price_range is required")
    elif mode == "none":
        if not data.get("no_product_site_type"):
            errors.append("no_product_site_type is required")
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False))


if __name__ == "__main__":
    main()
