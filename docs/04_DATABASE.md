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

# Physical Schema Specification

## core.locality

Purpose:
Represents a named Bengaluru locality used as the geographic grouping for properties and amenities.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| locality_id | UUID | PRIMARY KEY | Unique locality identifier |
| name | VARCHAR(120) | NOT NULL | Locality name |
| city | VARCHAR(80) | NOT NULL | City name |
| state | VARCHAR(80) | NOT NULL | State name |
| pincode | VARCHAR(10) | NULL | Postal code |
| latitude | DOUBLE PRECISION | NULL | Representative latitude |
| longitude | DOUBLE PRECISION | NULL | Representative longitude |
| geometry | GEOMETRY(MULTIPOLYGON, 4326) | NULL | Geographic boundary of the locality |
| description | TEXT | NULL | Human-readable locality description |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### Constraints

- `name`, `city`, and `state` are required.
- `(name, city, state)` must be unique.
- `latitude` must be between -90 and 90 when provided.
- `longitude` must be between -180 and 180 when provided.
- Geometry uses SRID 4326 (WGS 84).

### Planned Indexes

- Unique B-tree index on `(name, city, state)`.
- GiST spatial index on `geometry`.

## core.property

Purpose:
Represents a unique physical residential property independent of any individual rental listing or scraping source.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| property_id | UUID | PRIMARY KEY | Unique property identifier |
| locality_id | UUID | NOT NULL, FOREIGN KEY | Locality containing the property |
| property_name | VARCHAR(200) | NULL | Apartment, building, or society name |
| address | TEXT | NOT NULL | Normalized property address |
| latitude | DOUBLE PRECISION | NOT NULL | Property latitude |
| longitude | DOUBLE PRECISION | NOT NULL | Property longitude |
| geometry | GEOMETRY(POINT, 4326) | NOT NULL | Exact geospatial location |
| property_type | VARCHAR(50) | NOT NULL | Residential property category |
| bhk | SMALLINT | NULL | Number of bedrooms |
| furnishing | VARCHAR(30) | NULL | Furnishing category |
| parking | BOOLEAN | NULL | Parking availability |
| bathrooms | SMALLINT | NULL | Number of bathrooms |
| area_sqft | NUMERIC(10,2) | NULL | Property area in square feet |
| floor | SMALLINT | NULL | Property floor |
| total_floors | SMALLINT | NULL | Total floors in building |
| facing | VARCHAR(20) | NULL | Property orientation |
| age_of_property | SMALLINT | NULL | Approximate age in years |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### Relationships

- Many properties can belong to one locality.
- `locality_id` references `core.locality(locality_id)`.

### Constraints

- Latitude must be between -90 and 90.
- Longitude must be between -180 and 180.
- `bhk` must be greater than 0 when provided.
- `bathrooms` must be greater than or equal to 0 when provided.
- `area_sqft` must be greater than 0 when provided.
- `floor` must be greater than or equal to 0 when provided.
- `total_floors` must be greater than or equal to 0 when provided.
- `age_of_property` must be greater than or equal to 0 when provided.
- `floor` cannot exceed `total_floors` when both are provided.
- Geometry uses SRID 4326 (WGS 84).

### Planned Indexes

- B-tree index on `locality_id`.
- GiST spatial index on `geometry`.
- B-tree index on `property_type`.


## core.listing

Purpose:
Represents a rental advertisement for a property published by an external source. A single physical property may have multiple listings across different platforms or over time.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| listing_id | UUID | PRIMARY KEY | Internal unique listing identifier |
| property_id | UUID | NOT NULL, FOREIGN KEY | Physical property represented by the listing |
| scrape_source_id | UUID | NOT NULL, FOREIGN KEY | Source platform from which the listing originated |
| external_listing_id | VARCHAR(255) | NOT NULL | Listing identifier assigned by the source platform |
| listing_url | TEXT | NOT NULL | Original listing URL |
| title | VARCHAR(300) | NULL | Listing title |
| description | TEXT | NULL | Listing description |
| rent | NUMERIC(12,2) | NOT NULL | Current monthly rent |
| deposit | NUMERIC(12,2) | NULL | Security deposit |
| maintenance | NUMERIC(12,2) | NULL | Monthly maintenance charge |
| available_from | DATE | NULL | Date from which the property is available |
| furnishing_status | VARCHAR(30) | NULL | Furnishing state advertised by the listing |
| listing_status | VARCHAR(30) | NOT NULL | Current listing lifecycle status |
| first_seen | TIMESTAMPTZ | NOT NULL | First time NIVAAS observed the listing |
| last_seen | TIMESTAMPTZ | NOT NULL | Most recent time NIVAAS observed the listing |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last record update timestamp |

### Relationships

- Many listings can represent one property.
- `property_id` references `core.property(property_id)`.
- Many listings can originate from one scrape source.
- `scrape_source_id` references the entity representing the external scraping source.

### Constraints

- `(scrape_source_id, external_listing_id)` must be unique.
- `rent` must be greater than 0.
- `deposit` must be greater than or equal to 0 when provided.
- `maintenance` must be greater than or equal to 0 when provided.
- `last_seen` cannot occur before `first_seen`.
- `listing_status` must use an approved lifecycle value.

### Planned Indexes

- Unique B-tree index on `(scrape_source_id, external_listing_id)`.
- B-tree index on `property_id`.
- B-tree index on `scrape_source_id`.
- B-tree index on `listing_status`.
- B-tree index on `rent`.
- B-tree index on `last_seen`.

## core.amenity

Purpose:
Represents a physical point of interest used by NIVAAS to evaluate accessibility, convenience, transit, healthcare, education, lifestyle, and other livability characteristics.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| amenity_id | UUID | PRIMARY KEY | Unique amenity identifier |
| locality_id | UUID | NULL, FOREIGN KEY | Locality associated with the amenity |
| name | VARCHAR(255) | NOT NULL | Amenity name |
| amenity_type | VARCHAR(50) | NOT NULL | Amenity category |
| address | TEXT | NULL | Human-readable address |
| latitude | DOUBLE PRECISION | NOT NULL | Amenity latitude |
| longitude | DOUBLE PRECISION | NOT NULL | Amenity longitude |
| geometry | GEOMETRY(POINT, 4326) | NOT NULL | Exact geospatial location |
| osm_id | BIGINT | NULL | OpenStreetMap object identifier when available |
| rating | NUMERIC(3,2) | NULL | External rating when available |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### Relationships

- A locality can be associated with many amenities.
- `locality_id` references `core.locality(locality_id)`.

### Constraints

- Latitude must be between -90 and 90.
- Longitude must be between -180 and 180.
- `rating` must be between 0 and 5 when provided.
- Geometry uses SRID 4326 (WGS 84).
- `amenity_type` must use an approved category.

### Planned Indexes

- B-tree index on `locality_id`.
- B-tree index on `amenity_type`.
- GiST spatial index on `geometry`.
- B-tree index on `osm_id` when provided.

## core.price_history

Purpose:
Stores historical monetary values observed for a listing so NIVAAS can analyze rent, deposit, and maintenance changes over time.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| price_history_id | UUID | PRIMARY KEY | Unique history record identifier |
| listing_id | UUID | NOT NULL, FOREIGN KEY | Listing whose price was observed |
| rent | NUMERIC(12,2) | NOT NULL | Observed monthly rent |
| deposit | NUMERIC(12,2) | NULL | Observed security deposit |
| maintenance | NUMERIC(12,2) | NULL | Observed monthly maintenance |
| recorded_at | TIMESTAMPTZ | NOT NULL | Time the values were observed |

### Relationships

- One listing can have many price-history records.
- `listing_id` references `core.listing(listing_id)`.

### Constraints

- `rent` must be greater than 0.
- `deposit` must be greater than or equal to 0 when provided.
- `maintenance` must be greater than or equal to 0 when provided.
- A listing should not contain duplicate price observations for the same `recorded_at`.

### Planned Indexes

- B-tree index on `listing_id`.
- B-tree index on `(listing_id, recorded_at)`.
- B-tree index on `recorded_at`.


## core.availability_history

Purpose:
Stores historical listing availability states so NIVAAS can track listing lifecycle, market activity, and how long rental opportunities remain available.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| availability_history_id | UUID | PRIMARY KEY | Unique history record identifier |
| listing_id | UUID | NOT NULL, FOREIGN KEY | Listing whose availability was observed |
| status | VARCHAR(30) | NOT NULL | Availability state at observation time |
| available_from | DATE | NULL | Advertised availability date |
| recorded_at | TIMESTAMPTZ | NOT NULL | Time the availability state was observed |

### Relationships

- One listing can have many availability-history records.
- `listing_id` references `core.listing(listing_id)`.

### Constraints

- `status` must use an approved lifecycle value.
- A listing should not contain duplicate availability observations for the same `recorded_at`.

### Planned Indexes

- B-tree index on `listing_id`.
- B-tree index on `(listing_id, recorded_at)`.
- B-tree index on `status`.
- B-tree index on `recorded_at`.

# ELT Layer

## metadata.scrape_source

Purpose:
Represents an external platform or provider from which NIVAAS collects rental listing data.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| scrape_source_id | UUID | PRIMARY KEY | Unique source identifier |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Human-readable source name |
| website | TEXT | NULL | Public website URL |
| base_url | TEXT | NULL | Base URL used by the scraper |
| active | BOOLEAN | NOT NULL | Whether collection from the source is enabled |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

### Constraints

- `name` must be unique.
- `active` should default to true during implementation.

### Planned Indexes

- Unique B-tree index on `name`.
- B-tree index on `active`.


## metadata.scrape_run

Purpose:
Represents one execution of a scraper against a specific external source.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| scrape_run_id | UUID | PRIMARY KEY | Unique scraper execution identifier |
| scrape_source_id | UUID | NOT NULL, FOREIGN KEY | Source scraped during the run |
| started_at | TIMESTAMPTZ | NOT NULL | Run start time |
| completed_at | TIMESTAMPTZ | NULL | Run completion time |
| status | VARCHAR(30) | NOT NULL | Current execution status |
| listings_found | INTEGER | NULL | Number of listings collected |
| duration_seconds | NUMERIC(12,3) | NULL | Total execution duration |

### Relationships

- One scrape source can have many scrape runs.
- `scrape_source_id` references `metadata.scrape_source(scrape_source_id)`.

### Constraints

- `completed_at` cannot occur before `started_at`.
- `listings_found` must be greater than or equal to 0 when provided.
- `duration_seconds` must be greater than or equal to 0 when provided.
- `status` must use an approved pipeline lifecycle value.

### Planned Indexes

- B-tree index on `scrape_source_id`.
- B-tree index on `status`.
- B-tree index on `started_at`.


## raw.raw_listing

Purpose:
Stores the original listing payload exactly as collected before normalization, validation, deduplication, or transformation.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| raw_listing_id | UUID | PRIMARY KEY | Unique raw record identifier |
| scrape_run_id | UUID | NOT NULL, FOREIGN KEY | Scrape execution that produced the record |
| raw_payload | JSONB | NOT NULL | Original structured listing payload |
| scraped_at | TIMESTAMPTZ | NOT NULL | Time the listing was collected |
| processed | BOOLEAN | NOT NULL | Whether downstream processing has occurred |

### Relationships

- One scrape run can produce many raw listings.
- `scrape_run_id` references `metadata.scrape_run(scrape_run_id)`.

### Constraints

- `processed` should default to false during implementation.

### Planned Indexes

- B-tree index on `scrape_run_id`.
- B-tree index on `processed`.
- B-tree index on `scraped_at`.
- GIN index on `raw_payload` only if querying raw JSON becomes necessary.


# RAG Layer

## rag.document

Purpose:
Represents a source document ingested into the NIVAAS knowledge system for retrieval-augmented generation.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| document_id | UUID | PRIMARY KEY | Unique document identifier |
| title | VARCHAR(300) | NOT NULL | Human-readable document title |
| source | TEXT | NULL | Original source or URL |
| document_type | VARCHAR(50) | NOT NULL | Document category |
| content | TEXT | NULL | Original extracted textual content |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### Constraints

- `title` is required.
- `document_type` must use an approved category.

### Planned Indexes

- B-tree index on `document_type`.


## rag.document_chunk

Purpose:
Represents a retrievable segment of a document together with its vector embedding for semantic search.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| chunk_id | UUID | PRIMARY KEY | Unique chunk identifier |
| document_id | UUID | NOT NULL, FOREIGN KEY | Parent document |
| chunk_index | INTEGER | NOT NULL | Position of the chunk within the document |
| chunk_text | TEXT | NOT NULL | Text contained in the chunk |
| metadata | JSONB | NULL | Flexible chunk-level metadata |
| embedding | VECTOR | NULL | Semantic embedding generated from chunk text |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

### Relationships

- One document can contain many document chunks.
- `document_id` references `rag.document(document_id)`.

### Constraints

- `chunk_index` must be greater than or equal to 0.
- `(document_id, chunk_index)` must be unique.

### Planned Indexes

- B-tree index on `document_id`.
- Unique B-tree index on `(document_id, chunk_index)`.
- Vector similarity index on `embedding` after the embedding model and dimensionality are frozen.


# Computer Vision Layer

## core.image

Purpose:
Represents an image associated with a physical property and provides a stable reference for computer-vision analysis.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| image_id | UUID | PRIMARY KEY | Unique image identifier |
| property_id | UUID | NOT NULL, FOREIGN KEY | Property represented in the image |
| image_url | TEXT | NOT NULL | Image storage or source location |
| image_hash | VARCHAR(128) | NULL | Content hash used for deduplication |
| source | VARCHAR(100) | NULL | Origin of the image |
| uploaded_at | TIMESTAMPTZ | NOT NULL | Time the image entered NIVAAS |

### Relationships

- One property can have many images.
- `property_id` references `core.property(property_id)`.
- One image can have many image-analysis records.

### Constraints

- `image_url` is required.

### Planned Indexes

- B-tree index on `property_id`.
- B-tree index on `image_hash`.


## analytics.image_analysis

Purpose:
Stores outputs produced by computer-vision models for a property image while preserving the model execution history.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| analysis_id | UUID | PRIMARY KEY | Unique analysis identifier |
| image_id | UUID | NOT NULL, FOREIGN KEY | Image analyzed |
| model_name | VARCHAR(150) | NOT NULL | Model that generated the analysis |
| objects_detected | JSONB | NULL | Structured detected objects and associated metadata |
| cleanliness_score | NUMERIC(5,4) | NULL | Predicted cleanliness score |
| furnishing_score | NUMERIC(5,4) | NULL | Predicted furnishing score |
| quality_score | NUMERIC(5,4) | NULL | Predicted image/property quality score |
| analysis_timestamp | TIMESTAMPTZ | NOT NULL | Time the analysis was generated |

### Relationships

- One image can have many analyses.
- `image_id` references `core.image(image_id)`.

### Constraints

- Scores must be between 0 and 1 when provided.

### Planned Indexes

- B-tree index on `image_id`.
- B-tree index on `model_name`.
- B-tree index on `analysis_timestamp`.

# Machine Learning Layer

## feature_store.feature

Purpose:
Stores versioned, computed property features used by machine-learning models and analytical scoring pipelines.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| feature_id | UUID | PRIMARY KEY | Unique feature record identifier |
| property_id | UUID | NOT NULL, FOREIGN KEY | Property for which the feature was calculated |
| feature_name | VARCHAR(150) | NOT NULL | Name of the computed feature |
| feature_value | DOUBLE PRECISION | NOT NULL | Numeric feature value |
| created_at | TIMESTAMPTZ | NOT NULL | Time the feature value was generated |

### Relationships

- One property can have many feature records.
- `property_id` references `core.property(property_id)`.

### Constraints

- `feature_name` is required.
- A property may contain multiple historical values for the same feature.

### Planned Indexes

- B-tree index on `property_id`.
- B-tree index on `feature_name`.
- B-tree index on `(property_id, feature_name)`.
- B-tree index on `created_at`.


## analytics.prediction

Purpose:
Stores versioned outputs generated by machine-learning models for individual properties.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| prediction_id | UUID | PRIMARY KEY | Unique prediction identifier |
| property_id | UUID | NOT NULL, FOREIGN KEY | Property associated with the prediction |
| model_name | VARCHAR(150) | NOT NULL | Model that produced the prediction |
| prediction_type | VARCHAR(100) | NOT NULL | Type of prediction generated |
| prediction_value | DOUBLE PRECISION | NOT NULL | Numeric prediction output |
| confidence_score | NUMERIC(5,4) | NULL | Optional model confidence |
| predicted_at | TIMESTAMPTZ | NOT NULL | Time the prediction was generated |

### Relationships

- One property can have many predictions.
- `property_id` references `core.property(property_id)`.

### Constraints

- `confidence_score` must be between 0 and 1 when provided.

### Planned Indexes

- B-tree index on `property_id`.
- B-tree index on `model_name`.
- B-tree index on `prediction_type`.
- B-tree index on `(property_id, prediction_type, predicted_at)`.


# Platform Metadata Layer

## metadata.pipeline_run

Purpose:
Tracks executions of NIVAAS data, feature-engineering, ML, RAG, and other processing pipelines for observability and reproducibility.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| pipeline_run_id | UUID | PRIMARY KEY | Unique pipeline execution identifier |
| pipeline_name | VARCHAR(150) | NOT NULL | Pipeline being executed |
| started_at | TIMESTAMPTZ | NOT NULL | Execution start time |
| completed_at | TIMESTAMPTZ | NULL | Execution completion time |
| status | VARCHAR(30) | NOT NULL | Pipeline execution status |
| duration_seconds | NUMERIC(12,3) | NULL | Execution duration |

### Constraints

- `completed_at` cannot occur before `started_at`.
- `duration_seconds` must be greater than or equal to 0 when provided.
- `status` must use an approved pipeline lifecycle value.

### Planned Indexes

- B-tree index on `pipeline_name`.
- B-tree index on `status`.
- B-tree index on `started_at`.


## metadata.data_source

Purpose:
Catalogs external datasets, APIs, public-data providers, and other sources used throughout NIVAAS.

### Columns

| Column | PostgreSQL Type | Constraints | Purpose |
|---|---|---|---|
| data_source_id | UUID | PRIMARY KEY | Unique data-source identifier |
| source_name | VARCHAR(150) | NOT NULL | Human-readable source name |
| source_type | VARCHAR(50) | NOT NULL | Type of external source |
| api_endpoint | TEXT | NULL | API or service endpoint when applicable |
| license | VARCHAR(200) | NULL | Data usage or licensing information |
| refresh_frequency | VARCHAR(50) | NULL | Expected data refresh cadence |

### Constraints

- `source_name` must be unique.

### Planned Indexes

- Unique B-tree index on `source_name`.
- B-tree index on `source_type`.
