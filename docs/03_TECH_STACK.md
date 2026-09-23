# Technology Stack

## Overview

This document records the technologies actively used in NIVAAS and the role each technology plays within the platform.

NIVAAS is built as a full-stack urban intelligence platform combining data engineering, geospatial analytics, recommendation systems, and modern web development.

---

# Technology Summary

| Layer | Technologies |
|---------|---------|
| Frontend | React, TypeScript, TailwindCSS, Vite, TanStack Router |
| Backend | FastAPI, Python, Pydantic |
| Database | PostgreSQL, PostGIS, Supabase |
| Recommendation Engine | NumPy, scikit-learn |
| API Communication | Axios |
| State Management | Zustand |
| Infrastructure | Docker, Docker Compose |
| Deployment | Vercel, Render, Supabase |
| Version Control | Git, GitHub |

---

# Frontend

## React

Used to build the user interface through reusable components.

Responsibilities:

- Recommendation workflow
- Locality exploration
- Locality profiles
- Dashboard views

---

## TypeScript

Provides static typing across the frontend codebase.

Benefits:

- Improved maintainability
- Better developer tooling
- Reduced runtime errors

---

## TailwindCSS

Utility-first styling framework used throughout the frontend.

Benefits:

- Rapid UI development
- Consistent styling
- Reduced CSS complexity

---

## Vite

Frontend build tool and development server.

Benefits:

- Fast development startup
- Efficient production builds

---

## TanStack Router

Client-side routing solution.

Responsibilities:

- Page navigation
- Route management
- URL-based application state

---

## Zustand

Lightweight frontend state management.

Used for:

- Shared UI state
- Recommendation workflow state

---

## Axios

HTTP client used for communication with backend APIs.

---

# Backend

## FastAPI

Primary backend framework.

Responsibilities:

- REST APIs
- Request handling
- Recommendation endpoints
- Locality endpoints
- API documentation

---

## Pydantic

Used for:

- Request validation
- Response validation
- Configuration management

---

## Python

Core backend programming language.

Used for:

- API development
- Recommendation engine
- Feature engineering
- Data processing

---

# Database

## PostgreSQL

Primary relational database.

Stores:

- Localities
- Properties
- Listings
- Amenities
- Historical records
- Feature data

---

## PostGIS

Spatial extension for PostgreSQL.

Used for:

- Geospatial calculations
- Distance measurements
- Spatial analysis

---

## Supabase

Managed PostgreSQL platform used in production.

Responsibilities:

- Database hosting
- Managed infrastructure
- Database access

---

# Recommendation Engine

## NumPy

Used for numerical operations and vector processing.

---

## scikit-learn

Used for recommendation calculations.

Current usage:

- Cosine similarity
- Feature comparison
- Recommendation ranking

The recommendation engine is based on feature similarity rather than predictive machine learning models.

---

# Infrastructure

## Docker

Provides a reproducible local development environment.

Benefits:

- Consistent setup
- Environment isolation
- Simplified onboarding

---

## Docker Compose

Used to orchestrate local services during development.

---

# Deployment

## Vercel

Hosts the production frontend application.

---

## Render

Hosts the production FastAPI backend.

---

## Supabase

Hosts the production PostgreSQL + PostGIS database.

---

# Version Control

## Git

Source control system used throughout development.

---

## GitHub

Repository hosting, collaboration, and project management.

---

# Design Philosophy

Technology choices in NIVAAS follow several principles:

- Prefer simple solutions over unnecessary complexity.
- Use proven and well-supported tools.
- Keep operational overhead low.
- Prioritize maintainability and readability.
- Select technologies that directly support product requirements.

---

# Current Scope

The current implementation does not use:

- Apache Spark
- Kafka
- Airflow
- Kubernetes
- Redis
- MongoDB
- LangChain
- Vector Databases
- Deep Learning Models

These technologies may be evaluated in future versions if clear engineering requirements emerge.
