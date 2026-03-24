#!/usr/bin/env python3
import json
import sys


def main():
    data = json.loads(sys.stdin.read() or "{}")
    payload = {
        "site_brief": {
            "industry": data.get("industry"),
            "language": data.get("language") or "en",
            "style": data.get("style"),
        },
        "product_setup": {
            "mode": data.get("product_source_mode"),
            "criteria": data.get("product_ds_criteria") or {},
            "upload_status": data.get("product_upload_status"),
            "no_product_site_type": data.get("no_product_site_type"),
        },
        "build_ready": bool(data.get("base_confirmed") and data.get("product_phase_confirmed")),
    }
    print(json.dumps({"ok": True, "payload": payload}, ensure_ascii=False))


if __name__ == "__main__":
    main()
