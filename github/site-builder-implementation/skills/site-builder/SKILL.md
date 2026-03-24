---
name: site-builder
description: Collect site-building requirements in stages, confirm the site brief, branch into product sourcing, and prepare a normalized payload for site generation.
allowed-tools:
- get_skill_instructions
- get_skill_reference
- get_skill_script
metadata:
  version: 0.1.0
  owner: growth-platform
  compatibility: agno>=2.0
---

## When to use

Use this skill when the user wants to:
- create a new website
- generate an ecommerce or showcase site
- define a site brief before site generation
- choose a website style based on industry
- decide how products should be sourced before site building

## Goal

This skill helps the agent collect the minimum required information for site generation,
confirm the base site brief, then move into the product sourcing phase, and finally prepare
a normalized payload for the site-building executor.

## Required Base Information

The agent must collect the following base information:
- industry (required)
- language (optional, defaults to English)
- style (optional, but should be recommended from industry if not provided)

## Product Sourcing Modes

After the base site brief is confirmed, the agent must move into the product phase.
Supported product sourcing modes are:
- upload
- ds
- none

## Critical Rules

1. Industry is mandatory.
2. Language defaults to English if omitted.
3. Style should be recommended from industry when missing.
4. Product sourcing mode may be collected early if natural.
5. Base confirmation must NOT include product sourcing mode.
6. Product phase confirmation must happen separately.
7. The build phase cannot start until both base info and product phase are confirmed.
