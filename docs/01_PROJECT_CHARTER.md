# NIVAAS

## Project Charter

**Version:** 1.0.0
**Status:** Active Development
**Project Type:** Urban Intelligence & Rental Recommendation Platform
**Owner:** Zaiba Muskan
**Last Updated:** September 2026

---

# 1. Overview

NIVAAS is a Bengaluru-focused Urban Intelligence Platform that helps renters evaluate and compare localities using rental market data, geospatial analytics, accessibility metrics, amenity intelligence, and recommendation models.

Rather than focusing only on rental listings, NIVAAS combines multiple locality signals such as rental affordability, transportation access, amenities, density, and neighborhood characteristics to support informed housing decisions.

The project is designed as a portfolio application that demonstrates Data Engineering, Backend Engineering, Geospatial Analytics, Recommendation Systems, and modern full-stack application development.

---

# 2. Vision

Build a data-driven platform that helps renters understand and compare Bengaluru localities beyond rental price alone.

NIVAAS aims to provide locality intelligence, explainable recommendations, and neighborhood insights through a unified analytics platform.

---

# 3. Problem Statement

Rental information is fragmented across multiple platforms, making it difficult for users to compare localities objectively.

Finding a suitable place to live often requires evaluating multiple factors such as:

- Rental affordability
- Commute convenience
- Metro accessibility
- Amenities and services
- Healthcare access
- Lifestyle preferences
- Neighborhood density
- Livability indicators

Most rental platforms focus primarily on listings rather than helping users understand the surrounding locality.

NIVAAS addresses this problem by consolidating locality-level intelligence into a single platform.

---

# 4. Objectives

The project demonstrates practical experience with:

- Data Engineering
- ELT Pipelines
- Geospatial Analytics
- Feature Engineering
- Recommendation Systems
- PostgreSQL & PostGIS
- Backend API Development
- Full Stack Application Development
- Data Modeling
- System Design
- Containerization
- Cloud Deployment

---

# 5. Target Users

## Primary Users

- Students
- Working Professionals
- Families relocating within Bengaluru
- First-time renters

## Secondary Users

- Recruiters
- Data Engineers
- Backend Engineers
- ML Engineers
- Urban Analytics Enthusiasts

---

# 6. Core Capabilities

Version 1 includes:

1. Rental Intelligence
2. Locality Profiles
3. Locality Comparison
4. Livability Analysis
5. Metro Accessibility Analysis
6. Amenity Accessibility Analysis
7. Rental Market Insights
8. Recommendation Engine
9. Interactive Maps
10. Locality Scoring Framework

---

# 7. Scope

## Included

- Historical rental dataset
- Locality-level analytics
- Geospatial datasets
- PostgreSQL database
- PostGIS spatial analytics
- ELT pipelines
- Feature store
- Recommendation engine
- FastAPI backend
- React + TypeScript frontend
- Dockerized local development
- API endpoints for locality intelligence
- Locality scoring framework

## Excluded

The following are intentionally outside Version 1:

- User authentication
- Payments
- Property booking
- Property management
- Owner dashboards
- Rental agreements
- Mobile applications
- Real-time listing updates
- Multi-city support

---

# 8. Success Criteria

Version 1 is considered successful when the platform can:

- Store and manage rental market data
- Maintain locality-level feature data
- Generate locality recommendations
- Compare neighborhoods objectively
- Serve recommendations through APIs
- Display locality insights through the frontend
- Support geospatial analysis workflows
- Update locality features through repeatable pipelines
- Operate through a reproducible local development environment

---

# 9. Engineering Principles

The project follows these principles:

- Prefer simplicity over unnecessary complexity.
- Every technology should solve a real problem.
- Preserve historical data whenever possible.
- Use ELT for data transformation workflows.
- Keep architecture modular and maintainable.
- Separate data, business logic, and presentation layers.
- Design systems that are testable and extensible.
- Favor transparency and explainability in recommendations.
- Build features that can be expanded incrementally.

---

# 10. Out of Scope

NIVAAS is an analytics and recommendation platform.

It is not intended to become:

- A rental marketplace
- A brokerage platform
- A property management platform
- A payment platform
- A social platform
- A real-estate transaction platform

---

# 11. Roadmap

## Phase 1 — Data Platform

- Database design
- Data ingestion
- Data modeling
- ELT pipelines

## Phase 2 — Feature Engineering

- Locality feature generation
- Accessibility metrics
- Amenity analytics
- Livability metrics

## Phase 3 — Recommendation Engine

- Locality ranking
- Similarity calculations
- Recommendation scoring

## Phase 4 — Backend APIs

- FastAPI services
- Repository layer
- Analytics endpoints
- Recommendation endpoints

## Phase 5 — Frontend Experience

- Locality exploration
- Recommendation workflow
- Maps and visualizations
- Locality dashboards

## Phase 6 — Deployment

- Containerization
- Production configuration
- Cloud deployment
- Monitoring and maintenance

---

# 12. Revision Policy

This document defines the overall product vision, goals, scope, and guiding principles of NIVAAS.

Changes should only be made when product direction, business requirements, or project scope changes.

Implementation details, architecture decisions, database design, and technical specifications should be documented in their respective documents.
