# Integration Guide

## What this scaffold already includes

- multi-stage site requirement collection
- base confirmation and product confirmation separation
- product source branching: upload / ds / none
- payload building
- executor mapping:
  - ecommerce -> generate_ecommerce_site
  - showcase -> generate_showcase_site
- mock generator client with preview URL

## How to integrate into an existing repo

### 1. Copy files into your project
Recommended mapping:

- `skills/site-builder/` -> your skills directory
- `app/services/*.py` -> your service/runtime directory
- `tests/` -> your tests directory

### 2. Wire runtime entry
Your agent or API layer should instantiate:

```python
runtime = SiteBuilderRuntime()
result = runtime.handle_message(session_id, user_text)
```

Then return:
- `result["reply"]`
- `result["stage"]`
- optional `result["task"]`
- optional `result["build_job"]`

### 3. Replace the mock store
Replace `InMemorySiteBuilderStore` with your DB-backed store if you need persistence.

### 4. Replace the mock generator client
Replace `SiteGeneratorClient.submit_build_job()` with your real job submission API.

### 5. Optional: strengthen extractor
The current extractor is rule-based. For production, replace it with:
- LLM structured extraction
- rule-based fallback

## Known limitations

- `SiteBuilderExtractor` is intentionally lightweight
- style recommendation is static
- build payload shape may need adjustment to match your generator API
- no auth / tenancy / tracing included

## Minimal runtime contract

`handle_message(session_id, text)` returns:

```json
{
  "ok": true,
  "stage": "build_ready",
  "action": "build_ready",
  "state": {...},
  "site_blueprint": {...},
  "build_job": {...},
  "task": {...},
  "reply": "站点任务已提交，预览地址：https://..."
}
```
