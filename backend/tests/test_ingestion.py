import pytest
from app.services.ingestion import DocumentIngestionService

def test_chunking_logic():
    text = (
        "Cloud computing is the on-demand delivery of IT resources over the internet. "
        "With cloud computing, you don't need to make large upfront investments in hardware. "
        "Instead, you can provision exactly the right type and size of computing resources you need. "
        "You can access as many resources as you need, almost instantly, and only pay for what you use."
    )
    chunks = DocumentIngestionService.chunk_text(text, chunk_size=120, chunk_overlap=30)
    assert len(chunks) >= 2
    assert "Cloud computing" in chunks[0]

def test_empty_chunking():
    chunks = DocumentIngestionService.chunk_text("")
    assert chunks == []
