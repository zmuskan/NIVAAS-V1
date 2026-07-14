# Build Roadmap

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document defines the implementation plan for NIVAAS.

Development follows incremental milestones. Each sprint produces a working, testable deliverable.

---

# Development Strategy

The project is built from the data layer upward.

Development order:

1. Infrastructure
2. Database
3. ELT Pipeline
4. Data Collection
5. Feature Engineering
6. Machine Learning
7. Backend APIs
8. AI Assistant
9. Frontend
10. Deployment
11. Production Readiness

---

# Sprint 0 — Repository Foundation

## Objective

Establish project structure and engineering standards.

### Deliverables

- Repository initialized
- GitHub configured
- Folder structure finalized
- Documentation created
- Project Charter completed

**Status:** ✅ Completed

---

# Sprint 1 — Infrastructure Foundation

## Objective

Prepare the local development environment.

### Deliverables

- Docker installed
- Python virtual environment
- Docker Compose
- PostgreSQL
- PostGIS
- pgvector
- dbt configured

**Outcome**

A reproducible local development environment.

---

# Sprint 2 — Database Engineering

## Objective

Design and implement the production database.

### Deliverables

- Database schemas
- Alembic migrations
- Core tables
- Relationships
- Indexes
- Seed data

**Outcome**

Production-ready database.

---

# Sprint 3 — Data Collection

## Objective

Build reliable data ingestion.

### Deliverables

- Playwright scraper
- BeautifulSoup parser
- Raw data ingestion
- Retry logic
- Logging
- Rate limiting

**Outcome**

Automated collection of rental listings.

---

# Sprint 4 — ELT Pipeline

## Objective

Transform raw data into analytics-ready datasets.

### Deliverables

- dbt project
- Staging models
- Core models
- Analytics models
- Feature Store

**Outcome**

Clean, validated, version-controlled data.

---

# Sprint 5 — Machine Learning

## Objective

Develop predictive models.

### Deliverables

- Feature engineering
- Rent prediction model
- Recommendation engine
- Model evaluation
- Model serialization

**Outcome**

Production-ready ML inference.

---

# Sprint 6 — Backend Development

## Objective

Develop REST APIs.

### Deliverables

- FastAPI application
- API endpoints
- Validation
- Error handling
- Logging
- API documentation

**Outcome**

Stable backend services.

---

# Sprint 7 — AI & RAG

## Objective

Build the AI assistant.

### Deliverables

- Knowledge Base
- Document chunking
- Embeddings
- pgvector integration
- LangChain pipeline
- Gemini integration

**Outcome**

Context-aware conversational assistant.

---

# Sprint 8 — Frontend

## Objective

Develop the user interface.

### Deliverables

- Property search
- Filters
- Interactive maps
- Charts
- Recommendation dashboard
- AI assistant interface

**Outcome**

Complete user-facing application.

---

# Sprint 9 — Computer Vision

## Objective

Extract visual features from images.

### Deliverables

- Image processing
- Greenery estimation
- Building condition
- Road quality
- Feature extraction

**Outcome**

Visual features integrated into ML pipeline.

---

# Sprint 10 — Deployment

## Objective

Deploy the platform publicly.

### Deliverables

- Azure deployment
- GitHub Actions
- Docker containers
- Managed PostgreSQL
- Blob Storage
- Public URL

**Outcome**

Production deployment.

---

# Sprint 11 — Production Readiness

## Objective

Prepare the project for demonstration.

### Deliverables

- Unit tests
- Integration tests
- Performance improvements
- Security review
- Documentation review
- Demo dataset
- Resume updates

**Outcome**

Production-quality portfolio project.

---

# Success Criteria

Version 1.0 is complete when:

- Data updates automatically.
- ML models produce predictions.
- AI assistant answers locality questions.
- Public application is available.
- Documentation is complete.
- Tests pass.
- Deployment is stable.

---

# Engineering Principles

- Build one sprint at a time.
- Complete each sprint before starting the next.
- Keep documentation synchronized.
- Maintain production-quality standards.
- Avoid unnecessary technologies.
- Prioritize maintainability over complexity.

---

# Revision Policy

This roadmap should only change when project scope or priorities change.
