<p align="center">
  <img src="docs/images/screenshots/logo1.png" alt="NIVAAS Logo" width="120">
</p>

<h1 align="center">NIVAAS</h1>
<p align="center"><strong>Bangalore Livability Intelligence Platform</strong></p>
<p align="center">An urban intelligence platform that combines locality analytics, recommendation systems, and geospatial intelligence to help users discover the most suitable neighborhoods in Bangalore.</p>

---

## Demo

| Resource | Link |
|---|---|
| Live Application | <https://nivaas-nivaas1.vercel.app> |
| Frontend Walkthrough | Available in repository (`docs/video/nivaas_frontend_demo.mp4`) |

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Overview](#overview)
- [Dataset Scale](#dataset-scale)
- [User Journey](#user-journey)
- [Recommendation Engine](#recommendation-engine)
- [Locality Intelligence Features](#locality-intelligence-features)
- [System Architecture](#system-architecture)
- [Database Design](#database-design)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Problem Statement

Choosing where to live in Bangalore means reconciling constraints that don't live in one place: rent budget, commute distance to a specific workplace, proximity to hospitals and groceries, and neighborhood character. Listing portals filter on price and configuration but leave the rest of that reasoning to the user, manually, across dozens of localities.

NIVAAS treats this as a ranking problem, not a search problem: given a user's constraints, which localities actually fit best, and why.

## Overview

NIVAAS is designed as a data-driven recommendation platform where intelligence resides in engineered locality features, geospatial analytics, and ranking algorithms rather than LLM prompts. The conversational assistant acts as an interaction layer over the same recommendation engine.

- **Locality Intelligence Layer** — structured data on properties, listings, and metro infrastructure, standardized into comparable per-locality metrics.
- **Recommendation Engine** — converts a user's stated constraints into a feature-based query and ranks localities by fit.
- **Geospatial Analytics** — PostGIS-backed spatial queries (metro proximity, accessibility) underpin several of the locality metrics above.

**Niv Assistant**, the conversational interface, sits on top of these components as an interaction layer. It is not the recommendation logic — it is a UI convenience over the same engine described below.

NIVAAS is positioned as a recommendation system, geospatial analytics platform, and urban intelligence product rather than a chatbot-centric application.

## Dataset Scale

| Entity | Volume |
|---|---|
| Properties | 460+ |
| Listings | 500+ |
| Localities | 1,122+ |
| Metro Stations | 128+ |
| Recommendation Dimensions | 15+ |

## User Journey

The recommendation flow is a guided questionnaire rather than a search bar — the inputs required for a meaningful ranking (budget, commute origin, lifestyle weighting) are structured and multi-dimensional, which a single search field can't capture reliably.

<p align="center">
  <img src="docs/images/screenshots/01_landing_page.png" alt="Landing Page" width="600">
</p>

The user starts on the landing page, then moves into a short onboarding step before the questionnaire begins.

<p align="center">
  <img src="docs/images/screenshots/02_user_journey.png" alt="User Journey" width="440">
  <img src="docs/images/screenshots/03_user_journey_name.png" alt="User Journey - Name" width="440">
</p>

The questionnaire itself is split into focused steps — budget, commute, lifestyle, and preferences — rather than one long form, so each constraint is captured deliberately.

<p align="center">
  <img src="docs/images/screenshots/04_questionnaire_budget.png" alt="Budget Step" width="440">
  <img src="docs/images/screenshots/05_questionnaire_commute.png" alt="Commute Step" width="440">
</p>
<p align="center">
  <img src="docs/images/screenshots/06_questionnaire_lifestyle.png" alt="Lifestyle Step" width="440">
  <img src="docs/images/screenshots/07_questionnaire_preferences.png" alt="Preferences Step" width="440">
</p>

Once submitted, the constraint set is sent to the recommendation engine.

<p align="center">
  <img src="docs/images/screenshots/08_recommendation_loading.png" alt="Recommendation Loading" width="440">
  <img src="docs/images/screenshots/09_recommendation_results.png" alt="Recommendation Results" width="440">
</p>

Results are split between top matches and the remaining ranked candidates, so the strongest fits aren't buried in a long list.

<p align="center">
  <img src="docs/images/screenshots/10_top_localities.png" alt="Top Localities" width="440">
  <img src="docs/images/screenshots/11_rest_localities.png" alt="Remaining Localities" width="440">
</p>

Each locality can be inspected in detail — its score breakdown and the amenities driving that score.

<p align="center">
  <img src="docs/images/screenshots/12_locality_scores.png" alt="Locality Scores" width="440">
  <img src="docs/images/screenshots/13_locality_amenities.png" alt="Locality Amenities" width="440">
</p>

Niv Assistant is available throughout for follow-up questions against the same underlying data.

<p align="center">
  <img src="docs/images/screenshots/14_niv_assistant.png" alt="Niv Assistant" width="600">
</p>

## Recommendation Engine

<p align="center">
  <img src="docs/images/recommendation-pipeline.svg" alt="Recommendation Pipeline" width="850">
</p>

The pipeline runs in five stages:

1. **Candidate Retrieval** — localities are narrowed down using hard constraints (budget range, inventory availability) before any scoring happens, keeping the candidate set bounded.
2. **Feature Extraction** — each candidate locality's stored feature vector (rent, accessibility, density metrics) is pulled from the feature store.
3. **Scoring** — candidates are scored against the user's stated weighting across the recommendation dimensions.
4. **Similarity Ranking** — the user's constraint vector is compared against each candidate locality's feature vector using cosine similarity (scikit-learn), producing a ranked order.
5. **Result Assembly** — per-dimension sub-scores are returned alongside the final rank, so a result can be inspected rather than treated as a single opaque number.

Feature vectors and similarity computation are built with **NumPy** and **scikit-learn**; there is no deep learning or predictive modeling in the current pipeline — ranking is a similarity computation over engineered features, not a trained model.

## Locality Intelligence Features

Localities are evaluated across recommendation dimensions including:

- Affordability
- Connectivity
- Metro Accessibility
- Walkability
- Lifestyle
- Hospital Accessibility
- Grocery Accessibility
- Restaurant Density
- Inventory Availability
- Urban Convenience

These are computed once per locality and stored in the feature store, rather than recalculated per request — the recommendation engine consumes precomputed features at query time.

## System Architecture

<p align="center">
  <img src="docs/images/system-architecture.svg" alt="System Architecture" width="850">
</p>

- **React + TypeScript + TanStack Router + Vite** power the frontend experience.
- **FastAPI** serves recommendation, locality intelligence, and geospatial APIs.
- **Supabase PostgreSQL + PostGIS** store locality, property, listing, and spatial data.
- **Supabase** provides managed database infrastructure and data access for locality intelligence workflows.
- **Feature Store Tables** hold precomputed locality intelligence metrics used during recommendation.
- **Render** hosts and deploys backend API services.
- **Vercel** hosts and deploys the production frontend application.
- **Docker** provides a reproducible local development environment.
- **GitHub** manages source control and project collaboration.

## Database Design

<p align="center">
  <img src="docs/images/erd.svg" alt="Database ERD" width="850">
</p>

The schema is organized around **Localities** as the aggregation root — properties and listings each belong to a locality, and metro station data is used to compute locality-level accessibility metrics. Localities carry spatial geometry, which PostGIS uses to resolve proximity and accessibility relationships that feed directly into the feature store consumed by the recommendation engine.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, TailwindCSS, TanStack Router |
| Backend | FastAPI, Python |
| Database | Supabase PostgreSQL, PostGIS |
| Cloud Services | Supabase |
| Data & Analytics | NumPy, scikit-learn |
| State Management | Zustand |
| API Layer | Axios |
| Deployment | Vercel, Render |
| Infrastructure | Docker, GitHub |

## Project Structure

```text
NIVAAS-V1/
│
├── backend/
│   └── app/

├── frontend/
│   └── nivaas-frontend/
│       ├── src/
│       ├── public/
│       └── package.json

├── data/
├── db/
├── docs/
├── elt/
├── tests/
├── docker-compose.yml
└── README.md
```

## Getting Started

**Prerequisites:** Python 3.11+, Node.js 18+, Docker.

```bash
# Clone
git clone https://github.com/zmuskan/NIVAAS-V1.git
cd NIVAAS-V1

# Start PostgreSQL + PostGIS
docker compose up -d db

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd ../frontend/nivaas-frontend
npm install
cp .env.example .env      # set VITE_API_BASE_URL
npm run dev
```

Backend API docs: `http://localhost:8000/docs`
Frontend: `http://localhost:5173`

## Roadmap

- Formal evaluation of recommendation quality (currently validated by manual review, not an automated metric).
- Incorporate user feedback on recommendations as a future input to locality scoring.
- Expand geospatial accessibility coverage beyond metro stations.

## Author

**Zaiba Muskan**

- GitHub: https://github.com/zmuskan
- Project Repository: https://github.com/zmuskan/NIVAAS-V1
- Live Application: https://nivaas-nivaas1.vercel.app
