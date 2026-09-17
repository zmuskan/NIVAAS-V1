# Technology Stack

**Version:** 1.0.0

**Status:** Active

**Last Updated:** September 2026

---

# Purpose

This document records the technologies currently used in NIVAAS and the reason each technology exists in the system.

Only technologies that are actively used in the repository should be listed here.

---

# Technology Overview

| Layer | Technology |
|---------|---------|
| Language | Python, TypeScript |
| Backend | FastAPI, Pydantic, Psycopg |
| Database | PostgreSQL, PostGIS |
| Frontend | React, Vite, Tailwind CSS |
| Routing | TanStack Router |
| Machine Learning | Scikit-learn |
| AI | Gemini |
| Infrastructure | Docker, Docker Compose |
| Version Control | Git, GitHub |
| CI/CD | GitHub Actions |
| Development Tools | VS Code, Pre-Commit |

---

# Programming Languages

| Technology | Purpose |
|------------|----------|
| Python 3.12+ | Backend APIs, data pipelines, feature engineering, recommendation engine |
| TypeScript | Frontend application development |
| SQL | Database schema, migrations, analytics queries |

---

# Backend

## FastAPI

Purpose:

- REST APIs
- Dependency injection
- Request handling
- OpenAPI documentation

Reason:

FastAPI provides strong typing, excellent performance, and automatic API documentation.

---

## Pydantic

Purpose:

- Request validation
- Response validation
- Settings management

Reason:

Provides type safety across the backend.

---

## Psycopg 3

Purpose:

- PostgreSQL connectivity
- Query execution
- Connection pooling

Reason:

Official PostgreSQL driver for Python.

---

# Database

## PostgreSQL

Purpose:

Primary data storage layer.

Stores:

- Properties
- Listings
- Localities
- Amenities
- Historical data
- Feature store data

Reason:

Reliable relational database with strong ecosystem support.

---

## PostGIS

Purpose:

Spatial analytics and geographic calculations.

Examples:

- Distance calculations
- Metro accessibility
- Amenity proximity
- Geospatial aggregation

Reason:

Industry standard spatial extension for PostgreSQL.

---

# Frontend

## React

Purpose:

User interface development.

Reason:

Component-based architecture and strong ecosystem.

---

## TypeScript

Purpose:

Type-safe frontend development.

Reason:

Reduces runtime errors and improves maintainability.

---

## Vite

Purpose:

Frontend build system and development server.

Reason:

Fast startup and efficient development workflow.

---

## Tailwind CSS

Purpose:

Frontend styling.

Reason:

Rapid UI development with consistent design patterns.

---

## TanStack Router

Purpose:

Application routing.

Reason:

Type-safe route definitions and modern React integration.

---

# Machine Learning

## Scikit-learn

Purpose:

Recommendation and similarity calculations.

Current Usage:

- Cosine similarity
- Ranking logic
- Feature processing

Reason:

Widely adopted machine learning toolkit.

---

# Artificial Intelligence

## Gemini

Purpose:

Natural language interactions through Niv.

Examples:

- Locality questions
- Recommendation explanations
- Conversational assistance

Reason:

Provides natural language capabilities for the platform.

---

# Data Engineering

## ELT Pipelines

Purpose:

Move data through:

Raw → Staging → Core → Feature Store

Responsibilities:

- Data cleaning
- Normalization
- Validation
- Feature generation

Implementation:

Custom Python pipelines located in the `elt/` directory.

---

# Infrastructure

## Docker

Purpose:

Containerized development environment.

Reason:

Consistent execution across machines.

---

## Docker Compose

Purpose:

Local orchestration.

Current Services:

- PostgreSQL
- PostGIS

Reason:

Simple multi-service local setup.

---

# Version Control

## Git

Purpose:

Source control.

---

## GitHub

Purpose:

Repository hosting and collaboration.

---

## GitHub Actions

Purpose:

Future CI/CD automation.

Current Status:

Workflow structure exists in the repository.

---

# Development Tools

## VS Code

Primary development environment.

---

## Pre-Commit

Purpose:

Code quality checks before commits.

---

## EditorConfig

Purpose:

Consistent formatting across contributors.

---

# Technologies Not Currently Used

The following technologies may be evaluated in future versions but are not currently part of the implementation:

- Apache Spark
- Kafka
- Airflow
- Kubernetes
- Redis
- MongoDB
- OpenCV
- XGBoost
- SHAP
- LangChain

They should not be introduced unless a clear engineering requirement exists.

---

# Technology Selection Principles

- Prefer simple solutions over complex infrastructure.
- Adopt technologies only when they solve a real problem.
- Keep operational overhead low.
- Favor maintainability and readability.
- Use production-proven tools.

---

# Revision Policy

Update this document only when a technology is added, removed, or replaced in the codebase.
