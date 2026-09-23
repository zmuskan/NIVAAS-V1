# Database Design

## Overview

This document describes the database architecture used by NIVAAS.

NIVAAS uses PostgreSQL and PostGIS to store rental market data, locality intelligence data, geospatial information, recommendation features, and analytics outputs.

The database acts as the single source of truth for all platform components.

---

# Technology Stack

| Technology | Purpose |
|------------|----------|
| PostgreSQL | Primary relational database |
| PostGIS | Geospatial analytics and spatial queries |

---

# Design Principles

The database design follows several principles:

- Database as the source of truth
- Locality-centric data model
- Geospatial-first architecture
- ELT-driven transformations
- Historical data preservation
- Feature-based recommendation support
- Separation of operational and analytical workloads

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
