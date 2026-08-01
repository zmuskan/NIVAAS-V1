-- =====================================================
-- NIVAAS
-- RAG
-- =====================================================

CREATE TABLE IF NOT EXISTS rag.document (

    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    locality_id UUID
        REFERENCES core.locality(locality_id)
        ON DELETE SET NULL,

    title TEXT NOT NULL,

    source TEXT,

    content TEXT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE IF NOT EXISTS rag.document_chunk (

    chunk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    document_id UUID NOT NULL
        REFERENCES rag.document(document_id)
        ON DELETE CASCADE,

    chunk_index INTEGER NOT NULL,

    chunk_text TEXT NOT NULL,

    embedding VECTOR,

    metadata JSONB,

    created_at TIMESTAMPTZ DEFAULT NOW()

);
