# Smoke Test Source

<!-- source_sha256: 1b81600fdd13aa0f234e0e70faabc33e717ac881a2a8c503ab72fe75ab37a2ee -->

## Summary

Diabetes is a chronic disease affecting blood glucose regulation, with type 2 diabetes commonly linked to insulin resistance and regular physical activity improving blood glucose control.

## Key Facts

- Diabetes is a chronic disease that affects how the body regulates blood glucose.
- Type 2 diabetes is commonly associated with insulin resistance.
- Regular physical activity can help improve blood glucose control.

## Entities

None identified.

## Concepts

- Diabetes
- Type 2 diabetes
- Insulin resistance

## Claims

- Diabetes is a chronic disease that affects how the body regulates blood glucose.
- Type 2 diabetes is commonly associated with insulin resistance.
- Regular physical activity can help improve blood glucose control.Get-Content "phase2\ingest.py" | Select-String "source_text|build_prompt|SOURCE DOCUMENT" -Context 5,10Get-Content "phase2\ingest.py" | Select-String "source_text|build_prompt|SOURCE DOCUMENT" -Context 5,10

## Source Reference

phase2/sources/smoke_source.md
