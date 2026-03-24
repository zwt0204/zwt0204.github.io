# Export Manifest

导出时间：2026-03-24

## 根目录

`/root/.openclaw/workspace/agents/code-engineer/site-builder-implementation/`

## 包含内容

### docs
- `README.md`
- `RUN.md`
- `INTEGRATION.md`
- `requirements-dev.txt`

### demo
- `demo.py`

### skill
- `skills/site-builder/SKILL.md`
- `skills/site-builder/references/conversation-flow.md`
- `skills/site-builder/references/style-recommendation-rules.md`
- `skills/site-builder/references/product-source-modes.md`
- `skills/site-builder/references/confirmation-rules.md`
- `skills/site-builder/references/state-schema.json`
- `skills/site-builder/scripts/suggest_styles.py`
- `skills/site-builder/scripts/validate_site_brief.py`
- `skills/site-builder/scripts/validate_product_phase.py`
- `skills/site-builder/scripts/normalize_product_input.py`
- `skills/site-builder/scripts/build_payload.py`

### app
- `app/__init__.py`
- `app/services/__init__.py`
- `app/services/site_builder_state.py`
- `app/services/site_builder_store.py`
- `app/services/site_builder_extractor.py`
- `app/services/site_builder_flow.py`
- `app/services/site_build_executor.py`
- `app/services/site_generator_client.py`
- `app/services/site_builder_runtime.py`

### tests
- `tests/__init__.py`
- `tests/test_site_builder_runtime.py`

## 当前状态

- 本地虚拟环境：`.venv/`
- 当前测试结果：`8 passed`

## 说明

默认不建议把 `.venv/` 一起分发到真实仓库。
如果只需要源码，请使用源码压缩包，不要复制虚拟环境。
