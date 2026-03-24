# Export Notes

## 推荐使用方式

如果你要把这套接入真实项目：

1. 解压源码包
2. 复制 `skills/site-builder/` 到你的 skills 目录
3. 复制 `app/services/` 到你的服务层目录
4. 复制 `tests/` 到你的测试目录
5. 按 `INTEGRATION.md` 接 runtime 入口

## 已实现规则摘要

- 基础信息收集：industry / language / style
- language 默认 `en`
- style 支持标准化，如 `高级极简 -> luxury minimal`
- 基础确认与商品确认分离
- 选品方式：`upload / ds / none`
- `upload / ds -> ecommerce`
- `none + showcase/brand/content -> showcase`
- 选品阶段支持修改并重确认
- 基础阶段支持修改并重确认
- 选品阶段明确修改行业时，回退到基础阶段
- 改行业时自动重算 `style_suggestions`，并清理旧 `style`
- `current_stage` 已持久化到 state
- runtime `build_ready` 返回 `site_blueprint / build_job / reply`
- `reset()` 真清状态
- `reply` 包含 `preview_url`

## 已验证

使用本地 `.venv` 跑过：

```bash
./.venv/bin/python -m pytest -q
```

结果：

```text
8 passed
```
