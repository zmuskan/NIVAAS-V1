# AI Context

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document provides essential project context for AI coding assistants.

Before generating code, AI assistants should use this document together with the Project Charter, Architecture, Development Rules, and Tech Stack documents.

---

# Project Overview

NIVAAS is a production-grade AI Urban Intelligence Platform that helps users discover and compare rental properties using geospatial analytics, machine learning, computer vision, and retrieval-augmented generation (RAG).

The project prioritizes engineering quality, maintainability, and production readiness over rapid feature development.

---

# Primary Objectives

- Build a real-world Data Science and ML Engineering portfolio project.
- Demonstrate modern ELT architecture.
- Build a modular and scalable system.
- Maintain production-quality code.
- Keep the architecture cloud-agnostic.
- Deploy publicly on Azure.

---

# Current Technology Stack

- Python
- PostgreSQL
- PostGIS
- pgvector
- dbt
- Playwright
- BeautifulSoup
- Pandas
- Polars
- XGBoost
- FastAPI
- Streamlit
- Docker
- GitHub Actions
- Azure
- Gemini
- LangChain
- OpenCV

Refer to `03_TECH_STACK.md` for implementation details.

---

# Development Principles

- Follow ELT architecture.
- Preserve historical data.
- Never overwrite raw data.
- Keep business logic separate from presentation.
- Build one feature at a time.
- Every technology must solve a real engineering problem.

---

# Repository Structure

```
backend/
frontend/
scrapers/
elt/
db/
ml/
cv/
rag/
docker/
tests/
scripts/
data/
docs/
```

Each directory has a single responsibility.

---

# Data Architecture

```
External Sources
        │
        ▼
RAW
        │
        ▼
STAGING
        │
        ▼
CORE
        │
        ▼
FEATURE STORE
        │
 ┌──────┴──────┐
 ▼             ▼
ML           RAG
```

---

# Coding Expectations

Generate code that is:

- Modular
- Readable
- Type-safe
- Production-ready
- Well documented
- Easy to test

Avoid unnecessary abstractions.

---

# Database Rules

- PostgreSQL is the source of truth.
- Use Alembic for migrations.
- Use SQLAlchemy for database access.
- Use PostGIS for spatial queries.
- Use pgvector for embeddings.

---

# API Rules

- FastAPI is the backend framework.
- Validate requests using Pydantic.
- Return meaningful HTTP status codes.
- Never expose secrets.
- Separate routes, services, and repositories.

---

# Machine Learning Rules

- Train models offline.
- Store serialized models.
- Never train models during API requests.
- Track evaluation metrics.
- Keep inference lightweight.

---

# AI Assistant Rules

When generating code:

- Read existing code before modifying it.
- Follow existing naming conventions.
- Reuse existing modules whenever possible.
- Avoid introducing new dependencies without justification.
- Update documentation when architecture changes.

---

# Constraints

Do not:

- Change the architecture.
- Replace approved technologies.
- Generate placeholder implementations.
- Introduce unnecessary frameworks.
- Duplicate existing functionality.

---

# Current Sprint

Refer to `PROJECT_STATUS.md` for the active sprint and current deliverables.

---

# Expected Output

Generated code should be:

- Ready for review
- Consistent with repository standards
- Easy to integrate
- Compatible with the existing architecture

---

# Revision Policy

Update this document only when project architecture, engineering standards, or development workflow changes.
