# Confirmation Rules

## Base Confirm
Only confirm:
- industry
- language
- style

Do not include product_source_mode in base confirmation.

## Product Confirm
Confirm:
- product_source_mode
- source-specific details

## Guard Rule
Messages like:
- 可以，不过改成...
- 行，但是换成...

must be treated as modification requests, not plain confirmations.
