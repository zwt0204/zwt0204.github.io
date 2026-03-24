# Site Builder Implementation Scaffold

这是基于昨天讨论整理出的完整实现骨架，包含：

- skill 层文档与 references
- scripts
- app/services 层代码骨架
- runtime 串联

## 目录

```text
site-builder-implementation/
├── skills/site-builder/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── app/services/
    ├── site_builder_state.py
    ├── site_builder_extractor.py
    ├── site_builder_flow.py
    ├── site_builder_store.py
    ├── site_build_executor.py
    ├── site_generator_client.py
    └── site_builder_runtime.py
```

## 说明

这是可运行骨架，不依赖你当前业务仓库结构。

如果你给我真实 repo 路径，我下一步可以继续做：
1. 对齐 import 路径
2. 接入你现有 skill loader / runtime
3. 修测试
4. 直接改到仓库里
