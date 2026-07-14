# Database Design

**Version:** 1.0.0
**Status:** Active
**Last Updated:** July 2026

---

# Purpose

This document defines the database architecture, schemas, data model, and storage strategy for NIVAAS.

The database is designed to support historical data, geospatial analytics, machine learning, and retrieval-augmented generation while maintaining data integrity and scalability.

---

# Database Platform

| Technology | Purpose |
|------------|---------|
| PostgreSQL | Primary relational database |
| PostGIS | Geospatial queries |
| pgvector | Vector embeddings for RAG |

---

# Database Principles

- PostgreSQL is the single source of truth.
- Raw data is immutable.
- Historical data is never deleted.
- ELT transforms data between layers.
- Every table has a clear ownership.
- Every record should be traceable to its source.

---

# Database Layers

```
RAW
│
├── Raw scraped data
├── API responses
└── External datasets

↓

STAGING

├── Cleaned data
├── Standardized values
└── Deduplicated records

↓

CORE

├── Business entities
├── Relationships
└── Historical tracking

↓

FEATURE STORE

├── ML Features
├── Engineered variables
└── Model inputs

↓

RAG

├── Documents
├── Chunks
└── Embeddings
```

---

# Database Schemas

| Schema | Purpose |
|----------|---------|
| raw | Original scraped data |
| staging | Cleaned intermediate data |
| core | Production business tables |
| feature_store | ML features |
| rag | Documents and embeddings |
| analytics | Aggregated reporting views |
| metadata | Pipeline metadata |

---

# Core Tables

## properties

Represents a unique physical property.

Stores:

- Location
- Coordinates
- Address
- Building information

One property may have multiple listings.

---

## listings

Represents an advertisement.

Stores:

- Rent
- Deposit
- Furnishing
- BHK
- Availability
- Source website

One property can have many listings.

---

## price_history

Stores historical rent changes.

Used for:

- Trend visualization
- Forecasting
- Price alerts

Historical records are never overwritten.

---

## localities

Stores locality-level information.

Examples:

- Whitefield
- HSR Layout
- Koramangala

Contains:

- Geometry
- Aggregate statistics

---

## amenities

Stores infrastructure data.

Examples:

- Metro stations
- Schools
- Hospitals
- Parks
- Grocery stores

Supports PostGIS distance calculations.

---

## environmental_metrics

Stores environmental information.

Examples:

- AQI
- Noise
- Greenery
- Temperature

Historical values retained.

---

## feature_store

Stores engineered ML features.

Examples:

- Walkability Score
- Metro Distance
- Livability Score
- Commute Time
- Green Cover
- Rental Growth

No raw data is stored here.

---

## knowledge_base

Stores RAG documents.

Examples:

- Locality descriptions
- Reviews
- Government reports
- Infrastructure summaries

---

## document_chunks

Stores chunked documents.

Each chunk is embedded independently.

---

## embeddings

Stores vector embeddings.

Technology:

pgvector

Used for semantic search.

---

# Relationships

```
Property
    │
    ├────────── Listings
    │               │
    │               └──────── Price History
    │
    ├────────── Feature Store
    │
    ├────────── Environmental Metrics
    │
    └────────── Amenities

Locality
      │
      ├──────── Properties
      └──────── Knowledge Base
```

---

# Spatial Data

All geographic entities use PostGIS.

Primary geometry type:

```
GEOMETRY(Point, 4326)
```

Typical operations:

- Distance calculations
- Radius search
- Commute analysis
- Nearest amenities
- Spatial joins

---

# Historical Data Strategy

NIVAAS keeps historical data.

Never:

- Delete listings
- Overwrite prices
- Replace raw data

Instead:

- Insert new records
- Track timestamps
- Mark inactive listings

This enables:

- Trend analysis
- Forecasting
- Market analytics

---

# Indexing Strategy

Indexes will be created for:

- Rent
- BHK
- Property ID
- Listing ID
- Locality
- Geometry
- Timestamp
- Vector embeddings

Spatial indexes use GiST.

---

# Data Quality Rules

The ELT pipeline is responsible for:

- Duplicate detection
- Missing values
- Type validation
- Coordinate validation
- Standardized locality names
- Source validation

---

# Database Security

- Parameterized queries only
- No hardcoded credentials
- Environment variables for connections
- Least-privilege database roles
- Database backups
- Migration-based schema management

---

# Migration Strategy

Database changes must use Alembic.

Direct schema edits are not permitted.

Every migration should be:

- Version controlled
- Reversible
- Documented

---

# Future Expansion

The database supports future additions including:

- Multi-city support
- User accounts
- Saved searches
- Notifications
- Feedback data
- Additional ML models

---

# Revision Policy

Changes to the database structure require corresponding updates to:

- Architecture
- ELT models
- Alembic migrations
- ADR documentation
