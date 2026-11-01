import pytest
from app.database import DatabaseManager, get_database
from app.services.vector_store import vector_store
from app.seed_data.course_seed import seed_course_data
from app.services.agent import copilot_agent

@pytest.mark.asyncio
async def test_database_and_rag_flow():
    # Connect
    await DatabaseManager.connect()
    db = get_database()
    assert db is not None
    
    # Seed
    await seed_course_data()
    
    # Search RAG
    results = await vector_store.search(query="six advantages of cloud computing", top_k=2)
    assert len(results) > 0
    assert "Module 1" in results[0]["module_title"]

    # Chat with Agent
    chat_res = await copilot_agent.process_chat(
        user_message="Explain the six advantages of cloud computing with examples."
    )
    assert chat_res["message"] is not None
    assert len(chat_res["citations"]) > 0
    assert len(chat_res["suggested_followups"]) > 0

    await DatabaseManager.close()
