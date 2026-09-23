# NIVAAS

## Project Charter

**Version:** 1.0.0
**Status:** Production Deployment
**Project Type:** Urban Intelligence & Rental Recommendation Platform
**Owner:** Zaiba Muskan
**Last Updated:** September 2026

---

# 1. Overview

NIVAAS is a Bengaluru-focused Urban Intelligence Platform that combines locality analytics, rental market intelligence, geospatial data, and recommendation algorithms to help users identify suitable neighborhoods based on their preferences and constraints.

The platform evaluates localities rather than individual properties, transforming locality-level data into structured intelligence that can be ranked, compared, and explored through a recommendation workflow.

NIVAAS serves as a portfolio project demonstrating Data Engineering, Backend Engineering, Recommendation Systems, Geospatial Analytics, Database Design, and Full Stack Development.

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

NIVAAS was built to demonstrate practical implementation of:

- Data Modeling
- PostgreSQL & PostGIS
- Feature Engineering
- Recommendation Systems
- Geospatial Analytics
- Backend API Development
- Frontend Application Development
- Cloud Deployment
- Containerized Development
- System Architecture Design
- End-to-End Data Products

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

1. Locality Intelligence Profiles
2. Rental Affordability Analysis
3. Recommendation Engine
4. Locality Ranking
5. Inventory Analysis
6. Density Analysis
7. Feature-Based Scoring
8. Explainable Recommendation Results
9. Locality Comparison Workflows
10. Conversational Assistant Interface

---

# 7. Scope

## Included

- Rental listing datasets
- Locality datasets
- Geospatial datasets
- PostgreSQL database
- PostGIS extensions
- Locality feature generation
- Feature store
- Recommendation engine
- FastAPI backend
- React + TypeScript frontend
- Dockerized development environment
- Supabase database deployment
- Render backend deployment
- Vercel frontend deployment
- Locality intelligence APIs

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

- Maintain locality intelligence datasets
- Generate locality-level features
- Rank localities using recommendation algorithms
- Produce explainable recommendation results
- Serve recommendations through APIs
- Display locality insights through the frontend
- Support geospatial data workflows
- Operate in a deployed cloud environment
- Support reproducible local development through Docker

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

# 11. Future Enhancements

Potential future enhancements include:

- Additional locality intelligence dimensions
- Improved recommendation personalization
- Enhanced geospatial analytics
- Automated data refresh workflows
- Expanded locality coverage
- Recommendation quality evaluation framework
- Advanced locality comparison dashboards

---

# 12. Revision Policy

This document defines the overall product vision, goals, boundaries, and guiding principles of NIVAAS.

Changes should only be made when product direction, business requirements, or project scope changes.

Implementation details, architecture decisions, database design, and technical specifications should be documented in their respective documents.
