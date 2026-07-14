# Technology Stack

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document records the technologies used in NIVAAS and the engineering rationale behind each selection.

Technologies are chosen based on project requirements, maintainability, industry adoption, and cost. New technologies should only be introduced when they solve a demonstrated problem.

---

# Programming Language

| Technology | Purpose | Reason |
|------------|---------|--------|
| Python 3.12+ | Primary development language | Strong ecosystem for Data Engineering, Machine Learning, APIs, and AI. |

---

# Data Collection

| Technology | Purpose | Reason |
|------------|---------|--------|
| Playwright | Dynamic web scraping | Handles JavaScript-heavy websites reliably. |
| BeautifulSoup | HTML parsing | Fast and lightweight HTML parsing after page rendering. |

---

# Data Processing

| Technology | Purpose | Reason |
|------------|---------|--------|
| Pandas | Data manipulation | Industry standard for tabular data processing. |
| Polars | High-performance processing | Faster processing for large datasets when required. |

---

# Data Platform

| Technology | Purpose | Reason |
|------------|---------|--------|
| PostgreSQL | Primary database | Reliable relational database with strong ecosystem. |
| PostGIS | Spatial analytics | Enables geospatial queries, routing, and location analysis. |
| pgvector | Vector storage | Stores embeddings for semantic search and RAG. |
| dbt | ELT transformations | Version-controlled SQL transformations and data modeling. |

---

# Machine Learning

| Technology | Purpose | Reason |
|------------|---------|--------|
| Scikit-learn | ML utilities | Preprocessing, evaluation, and baseline models. |
| XGBoost | Rent prediction | High-performance model for structured tabular data. |
| SHAP | Model explainability | Explains model predictions for transparency. |
| Joblib | Model serialization | Lightweight model persistence for deployment. |

---

# Computer Vision

| Technology | Purpose | Reason |
|------------|---------|--------|
| OpenCV | Image processing | Extract visual features from street and property images. |

---

# Generative AI

| Technology | Purpose | Reason |
|------------|---------|--------|
| Gemini | LLM | Natural language reasoning and responses. |
| LangChain | RAG orchestration | Connects retrieval pipeline with Gemini. |

---

# Backend

| Technology | Purpose | Reason |
|------------|---------|--------|
| FastAPI | REST API | High performance, async support, automatic API documentation. |
| Pydantic | Validation | Type-safe request and response validation. |
| SQLAlchemy | Database access | ORM and parameterized SQL support. |
| Alembic | Database migrations | Version-controlled schema changes. |

---

# Frontend

| Technology | Purpose | Reason |
|------------|---------|--------|
| Streamlit | User interface | Rapid development of interactive analytics dashboards. |
| Plotly | Visualization | Interactive charts and dashboards. |
| Folium | Mapping | Interactive geospatial visualization. |

---

# DevOps

| Technology | Purpose | Reason |
|------------|---------|--------|
| Docker | Containerization | Consistent local and production environments. |
| Docker Compose | Local orchestration | Manage multi-container development setup. |
| GitHub Actions | CI/CD | Automated testing and deployment workflows. |
| Git | Version control | Source code management. |
| GitHub | Repository hosting | Collaboration and project management. |

---

# Cloud

| Technology | Purpose | Reason |
|------------|---------|--------|
| Azure | Production deployment | Public cloud deployment and cloud engineering experience. |
| Azure Database for PostgreSQL *(or Neon during development)* | Managed database | Production-ready PostgreSQL hosting. |
| Azure Blob Storage | Object storage | Store scraped images and static assets. |

---

# Development Tools

| Technology | Purpose | Reason |
|------------|---------|--------|
| VS Code | IDE | Primary development environment. |
| pyproject.toml | Project configuration | Standard Python project configuration. |
| pre-commit | Code quality | Automated formatting and validation before commits. |
| EditorConfig | Consistent formatting | Standardizes editor behavior across environments. |

---

# Technologies Evaluated but Not Adopted

| Technology | Reason |
|------------|--------|
| Apache Spark | Dataset size does not require distributed computing. |
| Kafka | No real-time event streaming requirements. |
| Kubernetes | Adds operational complexity without clear benefit. |
| Airflow | Scheduled jobs can be handled with GitHub Actions. |
| MongoDB | PostgreSQL better supports relational and geospatial workloads. |
| Redis | Will only be introduced if performance profiling justifies caching. |

---

# Guiding Principles

- Prefer mature and widely adopted technologies.
- Minimize operational complexity.
- Keep the architecture cloud-agnostic where possible.
- Choose tools based on engineering requirements, not popularity.
- Favor maintainability and scalability over unnecessary complexity.

---

# Revision Policy

This document should only be updated when technologies are added, removed, or replaced.
