from __future__ import annotations

from typing import Any, Dict


class SiteGeneratorClient:
    def submit_build_job(self, build_job: Dict[str, Any]) -> Dict[str, Any]:
        job_type = build_job.get("job_type")
        suffix = "ecom" if job_type == "generate_ecommerce_site" else "showcase"
        return {
            "ok": True,
            "task_id": f"draft-{suffix}-001",
            "preview_url": f"https://preview.example.com/{suffix}/draft-001",
            "status": "submitted",
        }
