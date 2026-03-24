from __future__ import annotations

import re
from typing import Any, Dict


STYLE_NORMALIZATION = {
    "高级极简": "luxury minimal",
    "轻奢极简": "luxury minimal",
    "luxury minimal": "luxury minimal",
    "modern minimal": "modern minimal",
}

SHOWCASE_HINTS = ["展示站", "showcase", "品牌展示", "作品展示"]
UPLOAD_HINTS = ["upload", "上传", "商品表", "商品文件", "sku", "catalog"]
DS_HINTS = ["ds", "dropshipping", "代发", "选品"]
CONFIRM_WORDS = {"可以", "行", "没问题", "确认", "ok", "好的"}
MODIFICATION_HINTS = ["改成", "不过改", "但是改", "换成", "调整为"]


class SiteBuilderExtractor:
    def extract(self, text: str) -> Dict[str, Any]:
        text = (text or "").strip()
        lowered = text.lower()
        patch: Dict[str, Any] = {}

        industry = self._extract_industry(text)
        if industry:
            patch["industry"] = industry

        language = self._extract_language(text)
        if language:
            patch["language"] = language

        style = self._extract_style(text)
        if style:
            patch["style"] = style

        mode = self._extract_product_source_mode(text)
        if mode:
            patch["product_source_mode"] = mode

        ds_criteria = self._extract_ds_criteria(text)
        if ds_criteria:
            patch["product_ds_criteria"] = ds_criteria

        no_product_site_type = self._extract_no_product_site_type(text)
        if no_product_site_type:
            patch["no_product_site_type"] = no_product_site_type

        if self._looks_like_upload_ready(text):
            patch["product_upload_status"] = "received"

        if self._is_plain_confirmation(text):
            patch["plain_confirmation"] = True

        if self._has_modification_intent(text):
            patch["modification_intent"] = True
            if self._has_industry_modification_intent(text):
                patch["industry_modification_intent"] = True

        return patch

    def _extract_industry(self, text: str) -> str | None:
        mapping = {
            "珠宝": "jewelry",
            "jewelry": "jewelry",
            "beauty": "beauty",
            "美妆": "beauty",
            "electronics": "electronics",
            "3c": "electronics",
            "home decor": "home decor",
            "家居": "home decor",
            "家居装饰": "home decor",
        }
        lowered = text.lower()
        for k, v in mapping.items():
            if k in lowered or k in text:
                return v
        return None

    def _extract_language(self, text: str) -> str | None:
        lowered = text.lower()
        if "英文" in text or re.search(r"\ben\b|english", lowered):
            return "en"
        if "中文" in text or re.search(r"\bzh\b|chinese", lowered):
            return "zh"
        return None

    def _extract_style(self, text: str) -> str | None:
        for k, v in STYLE_NORMALIZATION.items():
            if k in text or k in text.lower():
                return v
        return None

    def _extract_product_source_mode(self, text: str) -> str | None:
        lowered = text.lower()
        if any(h in lowered or h in text for h in UPLOAD_HINTS):
            return "upload"
        if any(h in lowered or h in text for h in DS_HINTS):
            return "ds"
        if "先不做商品" in text or "不做商品" in text or "none" in lowered:
            return "none"
        return None

    def _extract_no_product_site_type(self, text: str) -> str | None:
        if "展示站" in text or "showcase" in text.lower():
            return "showcase"
        if "品牌站" in text:
            return "brand site"
        if "内容站" in text:
            return "content site"
        return None

    def _extract_ds_criteria(self, text: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        lowered = text.lower()

        if "home decor" in lowered:
            result["category"] = "home decor"
        elif "jewelry" in lowered:
            result["category"] = "jewelry"

        if "美区" in text or "美国" in text or re.search(r"\bus\b|united states", lowered):
            result["market"] = "US"
        elif "欧洲" in text or "eu" in lowered:
            result["market"] = "EU"

        price_match = re.search(r"(\d+\s*[-~到]\s*\d+\s*(usd|刀|美金|美元)?)", lowered)
        if price_match:
            result["price_range"] = price_match.group(1).replace("刀", "USD")

        qty_match = re.search(r"(\d+)\s*(个|款|sku)", text.lower())
        if qty_match:
            result["quantity_target"] = qty_match.group(1)

        return result

    def _looks_like_upload_ready(self, text: str) -> bool:
        return any(x in text.lower() for x in ["已上传", "上传了", "uploaded", "发你了"])

    def _has_modification_intent(self, text: str) -> bool:
        normalized = text.strip().lower()
        return any(h in normalized for h in MODIFICATION_HINTS)

    def _has_industry_modification_intent(self, text: str) -> bool:
        normalized = text.strip().lower()
        return any(x in normalized for x in ["行业改成", "行业换成", "站点行业改成", "站点行业换成", "不是做"]) 

    def _is_plain_confirmation(self, text: str) -> bool:
        normalized = text.strip().lower()
        if self._has_modification_intent(normalized):
            return False
        return normalized in CONFIRM_WORDS
