# Architecture Decisions

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document records significant architectural and engineering decisions made during the development of NIVAAS.

Each major decision should be documented as an Architecture Decision Record (ADR).

---

# Decision Index

| ADR | Title | Status |
|------|-------|--------|
| ADR-0001 | Adopt PostgreSQL as the primary database | Accepted |
| ADR-0002 | Adopt ELT over ETL | Accepted |
| ADR-0003 | Use Medallion-style layered architecture | Accepted |
| ADR-0004 | Use dbt for data transformations | Accepted |
| ADR-0005 | Use PostGIS for geospatial analytics | Accepted |
| ADR-0006 | Use pgvector for vector search | Accepted |
| ADR-0007 | Use FastAPI as backend framework | Accepted |
| ADR-0008 | Use Streamlit for Version 1 frontend | Accepted |
| ADR-0009 | Deploy using Docker containers | Accepted |
| ADR-0010 | Deploy production environment on Azure | Accepted |
| ADR-0011 | Use GitHub Actions for CI/CD | Accepted |
| ADR-0012 | Train ML models offline | Accepted |
| ADR-0013 | Store historical rental data | Accepted |
| ADR-0014 | Computer Vision as a feature source | Accepted |
| ADR-0015 | Gemini + LangChain for RAG | Accepted |

---

# Accepted Decisions

## ADR-0001

**Decision**

PostgreSQL is the primary database.

**Reason**

Supports relational, geospatial, and vector workloads in a single platform.

---

## ADR-0002

**Decision**

Adopt ELT instead of ETL.

**Reason**

Modern databases efficiently handle transformations while preserving raw data.

---

## ADR-0003

**Decision**

Use layered architecture.

```
RAW

↓

STAGING

↓

CORE

↓

FEATURE STORE
```

**Reason**

Improves maintainability and data lineage.

---

## ADR-0004

**Decision**

Use dbt.

**Reason**

Version-controlled SQL transformations and modular data models.

---

## ADR-0005

**Decision**

Use PostGIS.

**Reason**

Native geospatial analysis and spatial indexing.

---

## ADR-0006

**Decision**

Use pgvector.

**Reason**

Store embeddings within PostgreSQL instead of introducing a separate vector database.

---

## ADR-0007

**Decision**

Use FastAPI.

**Reason**

High performance, async support, automatic OpenAPI documentation, and strong typing.

---

## ADR-0008

**Decision**

Use Streamlit for Version 1.

**Reason**

Rapid development while keeping the focus on backend, ML, and data engineering.

---

## ADR-0009

**Decision**

Containerize the platform using Docker.

**Reason**

Consistent development and deployment environments.

---

## ADR-0010

**Decision**

Deploy on Azure.

**Reason**

Gain hands-on cloud deployment experience while keeping the application cloud-agnostic.

---

## ADR-0011

**Decision**

Use GitHub Actions.

**Reason**

Simple CI/CD integrated with the repository.

---

## ADR-0012

**Decision**

Train models offline.

**Reason**

Reduce production resource usage and keep inference lightweight.

---

## ADR-0013

**Decision**

Retain historical data.

**Reason**

Supports forecasting, trend analysis, and market analytics.

---

## ADR-0014

**Decision**

Computer Vision generates engineered features.

**Reason**

Image-derived insights improve recommendations but do not replace structured data.

---

## ADR-0015

**Decision**

Use Gemini with LangChain.

**Reason**

Provide explainable, retrieval-based responses grounded in project data.

---

# Future Decisions

Future architectural changes should be documented as additional ADRs.

Examples include:

- Multi-city expansion
- Authentication
- Mobile application
- Recommendation model upgrades
- Cloud migration
- Event-driven processing

---

# Decision Guidelines

Create a new ADR when a decision:

- Changes architecture
- Introduces a major dependency
- Alters deployment strategy
- Modifies the data platform
- Changes development workflow
- Affects long-term maintainability

---

# Revision Policy

Do not edit historical ADRs.

New decisions should be recorded as new ADRs to preserve project history.
