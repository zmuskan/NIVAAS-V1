-- =====================================================
-- NIVAAS Database Initialization
-- =====================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS feature_store;
CREATE SCHEMA IF NOT EXISTS rag;
CREATE SCHEMA IF NOT EXISTS metadata;

-- ============================================================
-- NIVAAS Database DDL
-- ============================================================

\i /docker-entrypoint-initdb.d/sql/001_metadata.sql
\i /docker-entrypoint-initdb.d/sql/002_core.sql
\i /docker-entrypoint-initdb.d/sql/003_history.sql
\i /docker-entrypoint-initdb.d/sql/004_raw.sql
\i /docker-entrypoint-initdb.d/sql/005_rag.sql
\i /docker-entrypoint-initdb.d/sql/006_feature_store.sql
\i /docker-entrypoint-initdb.d/sql/007_analytics.sql
\i /docker-entrypoint-initdb.d/sql/008_indexes.sql
