from __future__ import annotations

from typing import Any, Dict

from .site_builder_extractor import SiteBuilderExtractor
from .site_builder_flow import SiteBuilderFlow
from .site_builder_state import SiteBuilderState
from .site_builder_store import InMemorySiteBuilderStore
from .site_build_executor import SiteBuildExecutor
from .site_generator_client import SiteGeneratorClient


class SiteBuilderRuntime:
    def __init__(
        self,
        store: InMemorySiteBuilderStore | None = None,
        extractor: SiteBuilderExtractor | None = None,
        flow: SiteBuilderFlow | None = None,
        executor: SiteBuildExecutor | None = None,
        generator_client: SiteGeneratorClient | None = None,
    ) -> None:
        self.store = store or InMemorySiteBuilderStore()
        self.extractor = extractor or SiteBuilderExtractor()
        self.flow = flow or SiteBuilderFlow()
        self.executor = executor or SiteBuildExecutor()
        self.generator_client = generator_client or SiteGeneratorClient()

    def handle_message(self, session_id: str, text: str) -> Dict[str, Any]:
        state = self.store.get_state(session_id)
        patch = self.extractor.extract(text)
        self._merge_patch(state, patch)
        step = self.flow.next_step(state)
        state.current_stage = step.get("stage") or state.current_stage

        if step["action"] != "build_ready":
            self.store.save_state(session_id, state)
            return self.make_response(state=state, step=step)

        payload = self.build_payload(state)
        exec_result = self.executor.execute(payload)
        submit_result = self.generator_client.submit_build_job(exec_result["build_job"])
        state.preview_url = submit_result.get("preview_url")
        self.store.save_state(session_id, state)
        return self.make_response(
            state=state,
            step=step,
            site_blueprint=exec_result["site_blueprint"],
            build_job=exec_result["build_job"],
            task=submit_result,
            reply=f"站点任务已提交，预览地址：{submit_result.get('preview_url')}",
        )

    def reset(self, session_id: str) -> Dict[str, Any]:
        self.store.reset_state(session_id)
        state = self.store.get_state(session_id)
        state.current_stage = "collect_industry"
        return self.make_response(
            state=state,
            step={"action": "reset", "stage": "collect_industry", "reply": "已重置。我们重新开始，先给我行业。"},
        )

    def build_payload(self, state: SiteBuilderState) -> Dict[str, Any]:
        return {
            "site_brief": {
                "industry": state.industry,
                "language": state.language or "en",
                "style": state.style,
            },
            "product_setup": {
                "mode": state.product_source_mode,
                "upload_status": state.product_upload_status,
                "criteria": state.product_ds_criteria.to_dict(),
                "no_product_site_type": state.no_product_site_type,
            },
            "build_ready": bool(state.base_confirmed and state.product_phase_confirmed),
        }

    def make_response(
        self,
        *,
        state: SiteBuilderState,
        step: Dict[str, Any],
        site_blueprint: Dict[str, Any] | None = None,
        build_job: Dict[str, Any] | None = None,
        task: Dict[str, Any] | None = None,
        reply: str | None = None,
    ) -> Dict[str, Any]:
        return {
            "ok": True,
            "stage": step.get("stage"),
            "action": step.get("action"),
            "state": state.to_dict(),
            "site_blueprint": site_blueprint,
            "build_job": build_job,
            "task": task,
            "reply": reply or step.get("reply"),
        }

    def _merge_patch(self, state: SiteBuilderState, patch: Dict[str, Any]) -> None:
        if "industry" in patch:
            industry_changed = patch["industry"] != state.industry
            state.industry = patch["industry"]
            if industry_changed:
                state.style_suggestions = self._suggest_styles(state.industry)
                if patch.get("industry_modification_intent"):
                    state.style = None
        if "language" in patch:
            state.language = patch["language"]
        if "style" in patch:
            state.style = patch["style"]
        if "product_source_mode" in patch:
            state.product_source_mode = patch["product_source_mode"]
        if "product_upload_status" in patch:
            state.product_upload_status = patch["product_upload_status"]
        if "no_product_site_type" in patch:
            state.no_product_site_type = patch["no_product_site_type"]
        if "base_confirmed" in patch:
            state.base_confirmed = patch["base_confirmed"]
        if "product_phase_confirmed" in patch:
            state.product_phase_confirmed = patch["product_phase_confirmed"]
        if patch.get("plain_confirmation"):
            if not state.base_confirmed:
                state.base_confirmed = True
            elif state.product_source_mode and not state.product_phase_confirmed:
                state.product_phase_confirmed = True
        if patch.get("modification_intent"):
            base_fields_changed = any(k in patch for k in ["industry", "language", "style"])
            product_fields_changed = any(
                k in patch for k in ["product_source_mode", "product_upload_status", "no_product_site_type", "product_ds_criteria"]
            )
            if patch.get("industry_modification_intent") and base_fields_changed:
                state.base_confirmed = False
                state.product_phase_confirmed = False
            elif product_fields_changed:
                state.product_phase_confirmed = False
            elif base_fields_changed and state.base_confirmed:
                state.base_confirmed = False
        if "product_ds_criteria" in patch:
            ds = patch["product_ds_criteria"] or {}
            if ds.get("category"):
                state.product_ds_criteria.category = ds["category"]
            if ds.get("market"):
                state.product_ds_criteria.market = ds["market"]
            if ds.get("price_range"):
                state.product_ds_criteria.price_range = ds["price_range"]
            if ds.get("style_constraints"):
                state.product_ds_criteria.style_constraints = ds["style_constraints"]
            if ds.get("quantity_target"):
                state.product_ds_criteria.quantity_target = ds["quantity_target"]

    def _suggest_styles(self, industry: str | None) -> list[str]:
        mapping = {
            "jewelry": ["luxury minimal", "premium editorial", "soft luxury", "visual storytelling"],
            "beauty": ["elegant clean", "premium editorial", "soft luxury"],
            "electronics": ["modern tech", "minimal dark", "precision clean"],
            "home decor": ["warm minimal", "editorial calm", "premium lifestyle"],
        }
        if not industry:
            return ["modern minimal", "premium clean", "editorial light"]
        return mapping.get(industry, ["modern minimal", "premium clean", "editorial light"])
