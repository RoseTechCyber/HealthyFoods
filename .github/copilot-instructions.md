# Copilot instructions for HealthyFoods

## Current repository reality
- This repository is currently a minimal scaffold: `README.md` + `LICENSE` only.
- Treat the project as **early-stage** and avoid assuming an existing framework, language, or deployment stack.
- Preserve the product intent documented in `README.md`: an AI-mediated food-order workflow (validation, payment, routing, delivery).

## Source of truth
- Product direction: `README.md`.
- Legal constraints: `LICENSE`.
- There are no additional agent rule files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) in this repo right now.

## How to make changes in this codebase
- Prefer small, foundational changes that establish structure (for example: initial app skeleton, docs, and basic tooling) over speculative feature depth.
- When adding new code, document assumptions in the same PR/change (because no architecture docs exist yet).
- Keep naming aligned with repository identity (`HealthyFoods`).
- Do not introduce multiple frameworks or polyglot stacks in one pass; choose one stack per iteration and keep it consistent.

## Workflow expectations
- No build, test, lint, or run commands are currently defined in-repo.
- If you add tooling, also add the canonical commands to `README.md` and keep them copy-paste runnable.
- When creating the first runnable setup, include:
  - dependency install command(s)
  - local run command
  - test command (if tests are introduced)
  - brief troubleshooting notes for missing prerequisites

## Architecture guidance for future edits
- Maintain a clear separation between:
  - user-facing ordering experience
  - AI decision/mediation logic
  - operational integrations (payment, routing, delivery providers)
- Prefer explicit interface boundaries between these areas, since integrations are central to the product statement in `README.md`.
- Record integration points early (provider name, auth method, request/response contracts) in docs as they are added.

## What to avoid
- Do not claim existing services, APIs, or infrastructure that are not present in the repository.
- Do not add generic “best practice” docs disconnected from actual code introduced in the same change.
- Do not rename the repository or rewrite product scope without explicit user request.