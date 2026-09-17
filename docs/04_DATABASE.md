# Database Design

**Version:** 1.0.0

**Status:** Active

**Last Updated:** September 2026

---

# Purpose

This document describes the database architecture used by NIVAAS.

The database supports:

- Rental listing storage
- Geospatial analytics
- Recommendation features
- Feature engineering

PostgreSQL serves as the single source of truth.

---

# Technology Stack

| Technology | Purpose |
|------------|----------|
| PostgreSQL | Primary relational database |
| PostGIS | Geospatial operations |

---

# Design Principles

- Database as source of truth
- Geospatial-first design
- Separation of raw and curated data
- Reproducible data pipelines
- Feature-driven recommendation architecture

---

# Database Architecture

```text
RAW
 │
 ▼
STAGING
 │
 ▼
CORE
 │
 ├── FEATURE_STORE
 │
 └── ANALYTICS
```

Each layer has a specific responsibility.

---

# Schemas

| Schema | Purpose |
|----------|----------|
| raw | Original collected data |
| staging | Cleaned and standardized data |
| core | Production entities |
| feature_store | Engineered recommendation features |
| analytics | Aggregated locality metrics |
| metadata | Pipeline tracking |

---

# Core Entities

## Locality

Represents a Bengaluru locality.

Examples:

- Whitefield
- Koramangala
- HSR Layout
- Indiranagar

Stores:

- Locality metadata
- Coordinates
- Spatial geometry

---

## Property

Represents a unique residential property.

Stores:

- Address information
- Property characteristics
- Geographic coordinates
- Spatial geometry

A property may have multiple listings.

---

## Listing

Represents a rental listing collected from an external source.

Stores:

- Rent
- Deposit
- Furnishing information
- Listing status

Multiple listings may reference the same property.

---

## Amenity

Represents points of interest used for locality analysis.

Examples:

- Metro Stations
- Hospitals
- Schools
- Restaurants
- Grocery Stores
- Parks

Used for accessibility calculations and recommendation features.

---

# Geospatial Model

NIVAAS uses PostGIS for spatial analysis.

Typical operations:

- Distance calculations
- Nearby amenity discovery
- Spatial joins
- Locality analysis

Common geometry types:

```sql
GEOMETRY(Point, 4326)

GEOMETRY(MultiPolygon, 4326)
```

---

# Feature Store

The feature store contains engineered features used by recommendation services.

Examples include:

- Average rent
- Rent range
- Property count
- Listing count
- Amenity density
- Density score
- Inventory score
- Overall score

Feature generation occurs through ELT pipelines.

---

# Recommendation Data Flow

```text
Property Data
        │
        ▼
Feature Engineering
        │
        ▼
Feature Store
        │
        ▼
Recommendation Engine
        │
        ▼
Ranked Localities
```

---

# Metadata

Metadata tables track:

- Pipeline runs
- Data sources
- Processing status

These tables support observability and reproducibility.

---

# Security

Database security principles:

- Environment-based configuration
- Parameterized queries
- Least-privilege access
- Migration-based schema changes

---

# Migration Strategy

Schema changes are managed through migrations.

Database structure should not be modified manually.

---

# Revision Policy

Update this document when:

- New schemas are introduced
- Core entities change
- Database architecture changes significantly

Implementation details belong in migrations and schema definitions.
