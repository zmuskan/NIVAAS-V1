# Development Rules

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# 1. Purpose

This document defines the engineering standards, development workflow, and quality expectations for NIVAAS.

All contributors and AI assistants must follow these rules.

---

# 2. Repository Workflow

- Development follows sprint-based milestones.
- Complete one feature before starting the next.
- Avoid parallel development unless required.
- Keep documentation synchronized with implementation.

---

# 3. Git Workflow

### Branches

- `main` – Production-ready code
- `develop` – Active development
- `feature/<feature-name>` – Individual features

Example

```
feature/playwright
feature/postgres
feature/dbt
feature/rag
```

---

# 4. Commit Convention

Use Conventional Commits.

Examples

```
feat(scraper): add NoBroker scraper

feat(db): create raw schema

fix(api): validate locality input

docs: update architecture

refactor(ml): simplify feature pipeline
```

Avoid generic messages such as:

```
Update

Fix

Changes
```

---

# 5. Coding Standards

- Write readable code.
- Prefer clarity over cleverness.
- Keep functions focused on one responsibility.
- Avoid duplicated logic.
- Use descriptive names.
- Add comments only when they improve understanding.

---

# 6. Python Standards

- Follow PEP 8.
- Use type hints where practical.
- Use virtual environments.
- Manage dependencies through `requirements.txt` and `pyproject.toml`.
- Validate formatting before committing.

---

# 7. Database Standards

- PostgreSQL is the single source of truth.
- Follow ELT architecture.
- Preserve raw data.
- Never overwrite historical records.
- Use migrations for schema changes.
- Avoid hardcoded SQL where an ORM or parameterized query is more appropriate.

---

# 8. Documentation Standards

Every significant feature must update:

- README (if user-facing)
- Architecture (if system changes)
- Tech Stack (if technology changes)
- Decisions (if architecture changes)

Documentation should explain **why**, not just **how**.

---

# 9. Security Standards

- Never commit `.env`.
- Never commit secrets or API keys.
- Validate all API inputs.
- Use parameterized SQL queries.
- Log errors without exposing sensitive information.
- Keep dependencies updated.

---

# 10. AI Usage Policy

AI tools may assist with:

- Code generation
- Refactoring
- Documentation
- Testing
- Debugging

Every generated output must be:

- Reviewed
- Understood
- Tested
- Integrated manually

The developer remains responsible for all code.

---

# 11. Testing Standards

Every completed feature should include:

- Basic validation
- Error handling
- Edge case testing
- Manual verification

Critical modules should include automated tests.

---

# 12. Definition of Done

A task is complete only when:

- Code is implemented.
- Tests pass.
- Documentation is updated.
- Changes are committed.
- No known critical issues remain.

---

# 13. Engineering Principles

- Build incrementally.
- Keep the architecture modular.
- Prefer maintainability over complexity.
- Introduce new technologies only when they solve a real problem.
- Optimize only after measuring performance.
- Design for future extensibility.

---

# Revision Policy

This document defines the engineering standards for NIVAAS and should only change when the team's development process changes.
