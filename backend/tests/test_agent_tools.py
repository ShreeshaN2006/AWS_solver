import pytest
from app.services.agent import CourseCopilotTools
from app.services.lab_service import COURSE_LABS

@pytest.mark.asyncio
async def test_tools_definitions():
    # Verify lab definitions
    assert len(COURSE_LABS) == 6
    lab_titles = [l["title"] for l in COURSE_LABS]
    assert "Introduction to AWS IAM" in lab_titles
    assert "Build your VPC and Launch a Web Server" in lab_titles
    assert "Introduction to Amazon EC2" in lab_titles
    assert "Working with EBS" in lab_titles
    assert "Build a Database Server" in lab_titles
    assert "Scale and Load Balance your Architecture" in lab_titles
