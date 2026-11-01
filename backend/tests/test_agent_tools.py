import pytest

from app.services import llm_provider, vector_store as vector_store_module
from app.services.agent import CourseCopilotTools
from app.services.lab_service import COURSE_LABS
from fastapi import HTTPException

from app.api.settings import get_system_settings, update_llm_provider
from app.config import settings
from app.services.llm_provider import LocalMockProvider, get_llm_provider
from app.services.vector_store import VectorStore


@pytest.mark.asyncio
async def test_tools_definitions():
    # Verify lab definitions
    assert len(COURSE_LABS) == 6
    lab_titles = [lab["title"] for lab in COURSE_LABS]
    assert "Introduction to AWS IAM" in lab_titles
    assert "Build your VPC and Launch a Web Server" in lab_titles
    assert "Introduction to Amazon EC2" in lab_titles
    assert "Working with EBS" in lab_titles
    assert "Build a Database Server" in lab_titles
    assert "Scale and Load Balance your Architecture" in lab_titles


def test_offline_provider_requires_explicit_selection():
    assert isinstance(get_llm_provider("local_mock"), LocalMockProvider)


def test_openai_provider_does_not_silently_fall_back_to_mock(monkeypatch):
    monkeypatch.setattr(llm_provider.settings, "OPENAI_API_KEY", None)
    with pytest.raises(RuntimeError, match="OpenAI provider is not configured correctly"):
        get_llm_provider("openai")


def test_vector_store_resolves_provider_when_used(monkeypatch):
    expected_provider = object()
    monkeypatch.setattr(
        vector_store_module,
        "get_llm_provider",
        lambda: expected_provider,
    )

    store = VectorStore()
    assert store.provider is expected_provider



@pytest.mark.asyncio
async def test_settings_api_does_not_return_database_uri():
    payload = await get_system_settings()
    assert "mongodb_uri" not in payload
    assert "mongodb_configured" in payload


@pytest.mark.asyncio
async def test_switching_to_openai_without_a_key_is_rejected(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    with pytest.raises(HTTPException) as error:
        await update_llm_provider(provider="openai")
    assert error.value.status_code == 400
