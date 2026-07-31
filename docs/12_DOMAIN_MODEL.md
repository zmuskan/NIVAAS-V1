# NIVAAS Domain Model

## Purpose

This document defines the business domain of NIVAAS.

The domain model is independent of PostgreSQL, FastAPI, Docker, or any implementation details.

The database, APIs, and machine learning pipeline must implement this model—not define it.

---

# Core Domain

- Property
- Listing
- Locality

# Infrastructure

- Amenity

# Historical

- PriceHistory
- AvailabilityHistory

# ELT

- ScrapeSource
- ScrapeRun
- RawListing

# Machine Learning

- Feature
- Prediction

# AI / RAG

- Document
- DocumentChunk

# Computer Vision

- Image
- ImageAnalysis

# Platform Metadata

- PipelineRun
- DataSource


# Entity Relationships
## Core

One Locality contains many Properties.

One Property can have many Listings.

One Listing belongs to exactly one Property.

---

## Historical

One Listing has many PriceHistory records.

One Listing has many AvailabilityHistory records.

---

## Infrastructure

One Locality contains many Amenities.

One Amenity belongs to one Locality.

---

## ELT

One ScrapeSource performs many ScrapeRuns.

One ScrapeRun produces many RawListings.

One RawListing can become one Listing after validation.

---

## Machine Learning

One Property has many Feature records.

One Property has many Predictions.

---

## AI / RAG

One Document contains many DocumentChunks.

---

## Computer Vision

One Property has many Images.

One Image has many ImageAnalysis records.


# Entity Attributes

## Locality

Primary Key
- locality_id (UUID)

Attributes
- name
- city
- state
- pincode
- latitude
- longitude
- geometry
- description
- created_at
- updated_at


## Property

Primary Key
- property_id (UUID)

Foreign Keys
- locality_id

Attributes
- property_name
- address
- latitude
- longitude
- geometry
- property_type
- bhk
- furnishing
- parking
- bathrooms
- area_sqft
- floor
- total_floors
- facing
- age_of_property
- created_at
- updated_at


## Listing

Primary Key
- listing_id (UUID)

Foreign Keys
- property_id
- scrape_source_id

Attributes
- external_listing_id
- listing_url
- title
- description
- rent
- deposit
- maintenance
- available_from
- furnishing_status
- listing_status
- first_seen
- last_seen
- created_at
- updated_at

## Amenity

Primary Key
- amenity_id (UUID)

Foreign Keys
- locality_id

Attributes
- name
- amenity_type
- address
- latitude
- longitude
- geometry
- osm_id
- rating
- created_at
- updated_at

## PriceHistory

Primary Key
- price_history_id (UUID)

Foreign Keys
- listing_id

Attributes
- rent
- deposit
- maintenance
- recorded_at

## AvailabilityHistory

Primary Key
- availability_history_id (UUID)

Foreign Keys
- listing_id

Attributes
- status
- available_from
- recorded_at

## ScrapeSource

Primary Key
- scrape_source_id (UUID)

Attributes
- name
- website
- base_url
- active
- created_at

## ScrapeRun

Primary Key
- scrape_run_id (UUID)

Foreign Keys
- scrape_source_id

Attributes
- started_at
- completed_at
- status
- listings_found
- duration_seconds

## RawListing

Primary Key
- raw_listing_id (UUID)

Foreign Keys
- scrape_run_id

Attributes
- raw_payload
- scraped_at
- processed

## Document

Primary Key
- document_id (UUID)

Attributes
- title
- source
- document_type
- content
- created_at
- updated_at

## DocumentChunk

Primary Key
- chunk_id (UUID)

Foreign Keys
- document_id

Attributes
- chunk_index
- chunk_text
- embedding
- created_at

## Image

Primary Key
- image_id (UUID)

Foreign Keys
- property_id

Attributes
- image_url
- image_hash
- source
- uploaded_at

## ImageAnalysis

Primary Key
- analysis_id (UUID)

Foreign Keys
- image_id

Attributes
- model_name
- objects_detected
- cleanliness_score
- furnishing_score
- quality_score
- analysis_timestamp

## Feature

Primary Key
- feature_id (UUID)

Foreign Keys
- property_id

Attributes
- feature_name
- feature_value
- created_at

## Prediction

Primary Key
- prediction_id (UUID)

Foreign Keys
- property_id

Attributes
- model_name
- prediction_type
- prediction_value
- confidence_score
- predicted_at

## PipelineRun

Primary Key
- pipeline_run_id (UUID)

Attributes
- pipeline_name
- started_at
- completed_at
- status
- duration_seconds

## DataSource

Primary Key
- data_source_id (UUID)

Attributes
- source_name
- source_type
- api_endpoint
- license
- refresh_frequency
