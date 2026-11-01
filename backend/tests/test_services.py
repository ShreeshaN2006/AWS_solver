from app.services.canvas_parser import canvas_parser
from app.services.document_ingestion import DocumentIngestionService
from app.services.retrieval import RetrievalService


def test_canvas_module_parsing():
    html = """
    <div class='context_module' id='context_module_1'>
      <div class='name'>Module 1 - Cloud Concepts Overview</div>
      <ul class='items'>
        <li class='context_module_item'><a href='/item/abc'>Lecture 1</a></li>
      </ul>
    </div>
    """
    items = canvas_parser.parse_modules(html)
    assert len(items) == 1
    assert items[0].module_id == "1"
    assert "Cloud Concepts" in items[0].module_title


def test_chunking_and_module_filtered_retrieval():
    ingestion = DocumentIngestionService()
    retrieval = RetrievalService()
    chunks = ingestion.build_chunks(
        course_id=183194,
        module_id="m4",
        module_title="AWS Cloud Security",
        document_name="security-guide",
        text="IAM helps control access and enforce least privilege across AWS services.",
    )
    retrieval.ingest(chunks)
    results = retrieval.search("least privilege", module_id="m4")
    assert results
    assert results[0].module_id == "m4"
