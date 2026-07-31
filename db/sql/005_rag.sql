-- ============================================================
-- NIVAAS
-- RAG Layer
-- ============================================================

CREATE TABLE rag.document (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(300) NOT NULL,
    source TEXT,
    document_type VARCHAR(50) NOT NULL,
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE rag.document_chunk (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_document_chunk_document
        FOREIGN KEY (document_id)
        REFERENCES rag.document(document_id),

    CONSTRAINT uq_document_chunk_index
        UNIQUE (document_id, chunk_index),

    CONSTRAINT chk_document_chunk_index
        CHECK (chunk_index >= 0)
);
