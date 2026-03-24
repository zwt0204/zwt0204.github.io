# Conversation Flow

## Stages

1. collect_industry
2. collect_style
3. confirm_base
4. collect_product_mode
5. collect_product_details
6. confirm_product
7. build_ready

## Base Confirmation

Base confirmation only confirms:
- industry
- language
- style

## Product Confirmation

Product confirmation confirms:
- product_source_mode
- upload product status OR ds criteria OR no-product site type

## Branches

### upload
Ask for product files, list, SKU set, or upload status.

### ds
Ask for:
- category
- market
- price_range
- optional style_constraints
- optional quantity_target

### none
Ask what type of site to build:
- brand site
- showcase site
- content site
- lead generation site
- coming soon page
