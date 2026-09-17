# NIVAAS Domain Model

## Purpose

This document defines the core business entities used by NIVAAS.

NIVAAS is an Urban Intelligence Platform that analyzes Bengaluru rental housing data and locality characteristics to generate explainable locality recommendations.

---

# Core Domain

- Locality
- Property
- Listing

---

# Supporting Domain

- Amenity

---

# Feature Store

- PropertyFeature
- LocalityFeature

---

# Entity Relationships

Locality
├── Property
│   ├── Listing
│   └── PropertyFeature
│
├── Amenity
│
└── LocalityFeature

---

## Locality

Represents a Bengaluru locality.

Examples:

- Whitefield
- Koramangala
- HSR Layout
- Indiranagar

Attributes:

- locality_id
- name
- geometry
- created_at
- updated_at

---

## Property

Represents a unique residential property.

Attributes:

- property_id
- locality_id
- address
- latitude
- longitude
- geometry
- property_type
- bhk
- furnishing
- bathrooms
- area_sqft

---

## Listing

Represents a rental listing associated with a property.

Attributes:

- listing_id
- property_id
- rent
- deposit
- maintenance
- listing_status
- first_seen
- last_seen

---

## Amenity

Represents nearby infrastructure used in livability analysis.

Examples:

- Hospital
- School
- Restaurant
- Grocery Store
- Park

Attributes:

- amenity_id
- locality_id
- amenity_type
- geometry

---

## PropertyFeature

Stores engineered property-level features used by recommendation services.

Attributes:

- feature_id
- property_id
- computed_at

---

## LocalityFeature

Stores engineered locality-level features used by recommendation services.

Attributes:

- feature_id
- locality_id
- computed_at

---

# Domain Principles

- Locality-centric analytics
- Geospatial intelligence
- Explainable recommendations
- Feature-driven ranking
- Separation of raw data and engineered features

---

# Revision Policy

Update this document when core entities or relationships change.
