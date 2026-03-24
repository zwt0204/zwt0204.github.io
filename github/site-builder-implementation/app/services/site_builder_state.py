from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ProductDsCriteria:
    category: Optional[str] = None
    market: Optional[str] = None
    price_range: Optional[str] = None
    style_constraints: Optional[str] = None
    quantity_target: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "market": self.market,
            "price_range": self.price_range,
            "style_constraints": self.style_constraints,
            "quantity_target": self.quantity_target,
        }


@dataclass
class SiteBuilderState:
    industry: Optional[str] = None
    language: str = "en"
    style: Optional[str] = None
    style_suggestions: list[str] = field(default_factory=list)
    base_confirmed: bool = False

    product_source_mode: Optional[str] = None
    product_upload_status: str = "not_started"
    product_ds_criteria: ProductDsCriteria = field(default_factory=ProductDsCriteria)
    no_product_site_type: Optional[str] = None
    product_phase_confirmed: bool = False

    build_payload_ready: bool = False
    current_stage: str = "collect_industry"
    preview_url: Optional[str] = None
    last_error: Optional[str] = None

    def reset(self) -> None:
        self.industry = None
        self.language = "en"
        self.style = None
        self.style_suggestions = []
        self.base_confirmed = False
        self.product_source_mode = None
        self.product_upload_status = "not_started"
        self.product_ds_criteria = ProductDsCriteria()
        self.no_product_site_type = None
        self.product_phase_confirmed = False
        self.build_payload_ready = False
        self.current_stage = "collect_industry"
        self.preview_url = None
        self.last_error = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "industry": self.industry,
            "language": self.language,
            "style": self.style,
            "style_suggestions": self.style_suggestions,
            "base_confirmed": self.base_confirmed,
            "product_source_mode": self.product_source_mode,
            "product_upload_status": self.product_upload_status,
            "product_ds_criteria": self.product_ds_criteria.to_dict(),
            "no_product_site_type": self.no_product_site_type,
            "product_phase_confirmed": self.product_phase_confirmed,
            "build_payload_ready": self.build_payload_ready,
            "current_stage": self.current_stage,
            "preview_url": self.preview_url,
            "last_error": self.last_error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SiteBuilderState":
        ds = data.get("product_ds_criteria") or {}
        return cls(
            industry=data.get("industry"),
            language=data.get("language") or "en",
            style=data.get("style"),
            style_suggestions=data.get("style_suggestions") or [],
            base_confirmed=bool(data.get("base_confirmed", False)),
            product_source_mode=data.get("product_source_mode"),
            product_upload_status=data.get("product_upload_status") or "not_started",
            product_ds_criteria=ProductDsCriteria(
                category=ds.get("category"),
                market=ds.get("market"),
                price_range=ds.get("price_range"),
                style_constraints=ds.get("style_constraints"),
                quantity_target=ds.get("quantity_target"),
            ),
            no_product_site_type=data.get("no_product_site_type"),
            product_phase_confirmed=bool(data.get("product_phase_confirmed", False)),
            build_payload_ready=bool(data.get("build_payload_ready", False)),
            current_stage=data.get("current_stage") or "collect_industry",
            preview_url=data.get("preview_url"),
            last_error=data.get("last_error"),
        )
