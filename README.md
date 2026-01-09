## Summary

API Gateway Referee is a referee-style decision tool that compares AWS API Gateway
options (HTTP API, REST API, WebSocket API) based on **explicit user constraints**
instead of static recommendations.

Rather than answering “Which API Gateway should I use?” with opinions,
the tool evaluates trade-offs and explains **why one option wins and what you give up**.

---

## Before vs After: Decision Clarity

### Before – Static Documentation & Ambiguity
Developers typically rely on:
- AWS documentation pages
- Blog posts with opinionated recommendations
- Incomplete comparisons that hide trade-offs

**Result:**  
Unclear decisions, over-engineering, or unnecessary cost.

![Homepage](screenshots/homepage-referee.png) Homepage framing the problem before comparison*

---

### After – Referee-Style Comparison
The referee evaluates options using explicit constraints:
- Budget
- Latency expectations
- Operational tolerance

It then produces:
- A clear **winner**
- A concise **why**
- Explicit **trade-offs (what you give up)**

![Compare Before](screenshots/compare-before.png)
![Compare After](screenshots/compare-after.png)
![Expanded JSON](screenshots/homepage-referee.png) showing raw scoring data

## How It Works

1. User provides constraints (budget, latency, ops tolerance)
2. The `/api/compare` endpoint evaluates each API Gateway option
3. A deterministic referee decision is returned
4. The UI renders both:
   - Human-readable explanation
   - Raw JSON for transparency

## Spec → Code Traceability (Kiro)

The decision logic is driven by a written specification:

`.kiro/specs/api-compare.md`

This spec defines:
- Compared options
- Decision criteria
- Expected inputs and outputs

Kiro is used to refine the spec and guide implementation.

![Kiro Spec](screenshots/kiro-spec.png) 
![Kiro Action](screenshots/kiro-action.png)



## Why This Matters

This project demonstrates:
- Clear problem framing
- Deterministic decision-making
- Trade-off transparency
- Spec-driven development

It prioritizes **clarity of reasoning** over feature count.
