from __future__ import annotations

from typing import Any, Dict


class SiteBuildExecutor:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        site_type = self._infer_site_type(payload)
        blueprint = {
            "site_type": site_type,
            "industry": payload.get("site_brief", {}).get("industry"),
            "language": payload.get("site_brief", {}).get("language"),
            "style": payload.get("site_brief", {}).get("style"),
            "product_setup": payload.get("product_setup", {}),
        }
        build_job = {
            "job_type": self._map_site_type_to_job_type(site_type),
            "payload": {
                "site_blueprint": blueprint,
                "generator_options": {
                    "draft": True,
                },
            },
        }
        return {
            "ok": True,
            "site_blueprint": blueprint,
            "build_job": build_job,
        }

    def _infer_site_type(self, payload: Dict[str, Any]) -> str:
        product_setup = payload.get("product_setup", {})
        mode = product_setup.get("mode")
        if mode in {"upload", "ds"}:
            return "ecommerce"
        site_type = product_setup.get("no_product_site_type") or "showcase"
        if site_type in {"showcase", "brand site", "content site"}:
            return "showcase"
        return "showcase"

    def _map_site_type_to_job_type(self, site_type: str) -> str:
        if site_type == "ecommerce":
            return "generate_ecommerce_site"
        return "generate_showcase_site"
