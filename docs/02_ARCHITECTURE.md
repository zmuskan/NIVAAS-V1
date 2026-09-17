# System Architecture

**Version:** 1.0.0
**Status:** Active
**Last Updated:** September 2026

---

# Purpose

This document describes the architecture of NIVAAS, the responsibilities of each system component, and how data flows through the platform.

NIVAAS follows a layered architecture that separates data ingestion, storage, feature engineering, recommendation logic, APIs, and user interfaces.

The goal is to keep the system modular, maintainable, and extensible while supporting future analytics and recommendation capabilities.

---

# High-Level Architecture

```text
                 External Data Sources
      (Rental Data, OSM, Metro, GeoSpatial Data)
                              │
                              ▼

                     Data Ingestion Layer
             (Loaders, Scrapers, Data Import Jobs)
                              │
                              ▼

                     PostgreSQL + PostGIS
                              │
                              ▼

                      ELT Pipelines
                              │
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼

   Raw Layer             Core Layer            Analytics Layer
      │                       │                       │
      └───────────────────────┴───────────────────────┘
                              │
                              ▼

                      Feature Store
                              │
                              ▼

                  Recommendation Engine
                              │
                              ▼

                        FastAPI APIs
                              │
                              ▼

                React + TypeScript Frontend
                              │
                              ▼

                           End Users
```

---

# Architectural Principles

The platform follows several core principles:

- Separation of concerns
- ELT-first data processing
- Database as the source of truth
- Modular service-oriented design
- Explainable recommendation logic
- Reproducible local development
- Future extensibility
- Minimal frontend business logic

---

# System Layers

---

# 1. Data Ingestion Layer

Responsible for collecting and loading datasets into the platform.

Sources include:

- Rental datasets
- OpenStreetMap data
- Metro station data
- Ward boundary datasets
- Locality reference datasets

Responsibilities:

- Data collection
- Data normalization
- Data validation
- Data loading

Output:

```text
Raw Database Tables
```

---

# 2. Database Layer

The database serves as the central storage layer.

Technology:

- PostgreSQL
- PostGIS

Responsibilities:

- Rental data storage
- Locality storage
- Amenity storage
- Metro data storage
- Spatial queries
- Historical data retention

The database acts as the single source of truth for all platform data.

---

# 3. ELT Layer

Responsible for transforming raw datasets into structured analytical models.

Responsibilities:

- Standardization
- Cleaning
- Deduplication
- Validation
- Aggregation
- Feature generation

Flow:

```text
Raw
 ↓
Staging
 ↓
Core
 ↓
Feature Store
```

---

# 4. Feature Store

The feature store contains engineered locality-level and property-level features used by downstream analytics and recommendation services.

Examples:

- Average rent
- Rent range
- Property density
- Amenity density
- Metro accessibility
- Hospital accessibility
- Restaurant density
- Walkability indicators
- Livability metrics

Responsibilities:

- Centralized feature storage
- Consistent analytics inputs
- Recommendation support

---

# 5. Recommendation Layer

Responsible for generating locality recommendations.

Inputs:

- User preferences
- Budget constraints
- Locality features
- Accessibility metrics
- Density metrics

Responsibilities:

- Candidate retrieval
- Similarity calculations
- Ranking
- Recommendation scoring
- Explainability

Output:

```text
Ranked Locality Recommendations
```

---

# 6. Backend Layer

Technology:

- FastAPI

Responsibilities:

- REST APIs
- Business logic
- Recommendation orchestration
- Analytics endpoints
- Locality profile endpoints
- Data validation

The backend acts as the interface between the database and frontend.

Frontend components never communicate directly with the database.

---

# 7. Frontend Layer

Technology:

- React
- TypeScript
- Tailwind CSS
- TanStack Router

Responsibilities:

- User onboarding flow
- Recommendation experience
- Locality exploration
- Interactive dashboards
- Locality profile pages
- Data visualization

The frontend is responsible only for presentation and user interaction.

Business logic remains in the backend.

---

# Core Data Flow

```text
External Sources
        ↓
Data Ingestion
        ↓
PostgreSQL + PostGIS
        ↓
ELT Pipelines
        ↓
Feature Store
        ↓
Recommendation Engine
        ↓
FastAPI
        ↓
React Frontend
        ↓
Users
```

---

# Recommendation Flow

```text
User Preferences
        ↓
Recommendation API
        ↓
Candidate Retrieval
        ↓
Feature Comparison
        ↓
Similarity Calculation
        ↓
Ranking
        ↓
Explanation Generation
        ↓
Response
```

---

# Repository Structure

```text
backend/
├── api/
├── services/
├── repositories/
├── schemas/
├── recommendation/
└── feature_engineering/

db/
├── schema/
├── migrations/
└── sql/

elt/
├── sources/
├── staging/
├── enrichment/
├── analytics/
└── features/

frontend/
└── nivaas-frontend/
```

---

# Local Development Architecture

```text
Developer
    │
    ▼

Docker PostgreSQL
    │
    ▼

FastAPI Backend
    │
    ▼

React Frontend
```

Development is designed to run entirely on a local machine using Docker and environment-based configuration.

---

# Security Principles

The platform follows several security practices:

- Environment-based configuration
- No secrets in source control
- Parameterized SQL queries
- Input validation through Pydantic
- Principle of least privilege
- Explicit API validation

---

# Design Decisions

The architecture intentionally:

- Uses PostgreSQL as the primary datastore.
- Uses PostGIS for spatial analysis.
- Separates repositories from services.
- Uses ELT instead of ETL.
- Maintains a dedicated feature store.
- Keeps recommendation logic independent of APIs.
- Separates frontend presentation from backend business logic.

---

# Future Extensions

The current architecture supports future additions such as:

- Additional Bengaluru datasets
- Advanced recommendation models
- Multi-city support
- User accounts
- Saved searches

---

# Revision Policy

Architectural changes should be documented in:

- Architecture documentation
- Database documentation
- Decision records

Major architectural decisions should also be reflected in:

`08_DECISIONS.md`
