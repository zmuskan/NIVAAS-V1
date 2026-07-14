# System Architecture

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document describes the overall architecture of NIVAAS, the responsibilities of each component, and how data flows through the system.

The architecture is designed to be modular, scalable, cloud-agnostic, and production-ready.

---

# High-Level Architecture

```
                    External Data Sources
      (NoBroker, Housing, MagicBricks, OSM, APIs)
                           │
                           ▼
            Playwright + BeautifulSoup Scrapers
                           │
                           ▼
                    RAW Data Layer
                  (PostgreSQL / PostGIS)
                           │
                           ▼
                  ELT Pipeline (dbt)
                           │
                           ▼
     ┌───────────────┬───────────────────┐
     ▼               ▼                   ▼
 STAGING         CORE MODELS      KNOWLEDGE BASE
     │               │                   │
     │               ▼                   ▼
     │         Feature Store         pgvector
     │               │                   │
     └───────────────┴──────────────┐
                                    ▼
                     ML + RAG Inference Layer
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            Recommendation Engine          Gemini Assistant
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                               FastAPI Backend
                                    │
                                    ▼
                            Streamlit Frontend
                                    │
                                    ▼
                                 End Users
```

---

# Architectural Principles

- Modular architecture
- ELT-first data processing
- Cloud-agnostic deployment
- Separation of concerns
- Immutable raw data
- Production-ready design
- Independent, testable components

---

# Component Responsibilities

## Data Collection

Responsible for collecting rental listings and external datasets.

### Responsibilities

- Scrape rental platforms
- Collect infrastructure data
- Collect environmental data
- Store raw responses

Output

```
RAW Layer
```

---

## ELT Layer

Responsible for transforming raw data into analytics-ready datasets.

### Responsibilities

- Data cleaning
- Standardization
- Deduplication
- Validation
- Feature generation

Output

```
Staging

↓

Core

↓

Feature Store
```

---

## Database Layer

Central storage for all project data.

Technologies

- PostgreSQL
- PostGIS
- pgvector

Responsibilities

- Transactional storage
- Spatial queries
- Historical tracking
- Vector storage

---

## Machine Learning Layer

Responsible for predictive analytics.

Models include

- Rent Prediction
- Livability Scoring
- Recommendation Engine

Responsibilities

- Training
- Evaluation
- Inference
- Explainability

---

## Computer Vision Layer

Responsible for extracting visual features.

Possible inputs

- Street imagery
- Property images
- Satellite imagery

Generated features

- Greenery
- Cleanliness
- Road quality
- Building condition

Outputs become structured ML features.

---

## RAG Layer

Responsible for answering locality-related questions.

Pipeline

```
Knowledge Base

↓

Embedding

↓

pgvector Search

↓

Context Retrieval

↓

Gemini

↓

Response
```

---

## Backend

Technology

FastAPI

Responsibilities

- REST APIs
- Authentication (future)
- Business logic
- ML inference
- RAG orchestration
- Validation

Frontend never communicates directly with the database.

---

## Frontend

Technology

Streamlit

Responsibilities

- Property search
- Interactive maps
- Filters
- Dashboards
- AI assistant interface

No business logic should exist in the frontend.

---

# Data Flow

```
Scrapers

↓

RAW

↓

dbt

↓

STAGING

↓

CORE

↓

Feature Store

↓

ML Models

↓

FastAPI

↓

Frontend
```

---

# AI Flow

```
User Question

↓

FastAPI

↓

Retriever

↓

pgvector

↓

Relevant Context

↓

Gemini

↓

Answer
```

---

# ML Flow

```
Feature Store

↓

Training

↓

Evaluation

↓

Serialized Model

↓

FastAPI

↓

Prediction
```

---

# Deployment Architecture

```
Developer

↓

GitHub

↓

GitHub Actions

↓

Azure

├── FastAPI

├── Streamlit

├── PostgreSQL

└── Blob Storage
```

Development uses Docker.

Production runs on Azure.

---

# Security Principles

- Secrets stored in environment variables
- Parameterized SQL queries
- Input validation using Pydantic
- HTTPS in production
- Principle of least privilege
- No secrets committed to Git

---

# Design Decisions

The architecture intentionally:

- Uses ELT instead of ETL.
- Keeps PostgreSQL as the single source of truth.
- Separates ML training from inference.
- Uses Docker for reproducibility.
- Keeps deployment cloud-agnostic.

---

# Future Extensions

The architecture supports future additions without major redesign.

Potential extensions include:

- Multi-city support
- Mobile application
- User accounts
- Reinforcement learning
- Advanced recommendation ranking
- Real-time notifications

---

# Revision Policy

Changes to this document require an architectural decision and should be reflected in `08_DECISIONS.md`.
