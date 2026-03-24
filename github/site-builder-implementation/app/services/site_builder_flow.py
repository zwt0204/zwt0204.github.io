from __future__ import annotations

from typing import Any, Dict

from .site_builder_state import SiteBuilderState


class SiteBuilderFlow:
    def next_step(self, state: SiteBuilderState) -> Dict[str, Any]:
        if not state.industry:
            return self._ask("collect_industry", "先给我行业。这个字段必填。")

        if not state.style:
            suggestions = state.style_suggestions or ["modern minimal", "premium clean", "editorial light"]
            return self._ask("collect_style", f"风格还没定。你可以直接选一个：{', '.join(suggestions)}")

        if not state.base_confirmed:
            return {
                "action": "confirm_base",
                "stage": "base_confirm",
                "reply": f"我先确认基础信息：行业={state.industry}，语言={state.language}，风格={state.style}。如果没问题你回复“确认”。",
            }

        if not state.product_source_mode:
            return self._ask("collect_product_mode", "接下来选品怎么走？支持 upload / ds / none。")

        if state.product_source_mode == "upload":
            if state.product_upload_status not in {"received", "confirmed"}:
                return self._ask("collect_upload_products", "把商品文件、SKU 或商品列表给我。")
        elif state.product_source_mode == "ds":
            ds = state.product_ds_criteria
            if not ds.category or not ds.market or not ds.price_range:
                return self._ask("collect_ds_criteria", "DS 还缺条件。至少给我 category、market、price_range。")
        elif state.product_source_mode == "none":
            if not state.no_product_site_type:
                return self._ask("collect_no_product_type", "不做商品的话，站点类型要定一下，比如 showcase / brand site / content site。")

        if not state.product_phase_confirmed:
            return {
                "action": "confirm_product",
                "stage": "product_confirm",
                "reply": self._build_product_confirm_reply(state),
            }

        state.build_payload_ready = True
        return {
            "action": "build_ready",
            "stage": "build_ready",
            "reply": "信息齐了，可以开始生成建站 payload 并提交建站任务。",
        }

    def _ask(self, stage: str, reply: str) -> Dict[str, Any]:
        return {"action": "ask", "stage": stage, "reply": reply}

    def _build_product_confirm_reply(self, state: SiteBuilderState) -> str:
        if state.product_source_mode == "upload":
            detail = f"upload，当前状态={state.product_upload_status}"
        elif state.product_source_mode == "ds":
            ds = state.product_ds_criteria
            detail = f"ds，category={ds.category}，market={ds.market}，price_range={ds.price_range}"
        else:
            detail = f"none，site_type={state.no_product_site_type}"
        return f"我再确认商品阶段信息：{detail}。如果没问题你回复“确认”。"
