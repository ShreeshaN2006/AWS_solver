import httpx
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("app.services.canvas_api")

class CanvasIntegrationService:
    """
    Read-only integration client for Instructure Canvas REST API.
    Strict Security Guarantees:
    - Never requests or stores student passwords.
    - Never scrapes session cookies.
    - Never submits quizzes or changes grades.
    - Read-only queries for modules, items, assignments, and completion states.
    """
    def __init__(self, base_url: Optional[str] = None, api_token: Optional[str] = None):
        self.base_url = (base_url or settings.CANVAS_BASE_URL).rstrip("/")
        self.api_token = api_token or settings.CANVAS_API_TOKEN

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_token:
            return {}
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }

    async def test_connection(self) -> Dict[str, Any]:
        """Verify API token credentials against the Canvas user profile endpoint."""
        if not self.api_token:
            return {
                "connected": False,
                "message": "No Canvas API token configured. Operating in fallback document import mode.",
                "fallback_active": True
            }

        url = f"{self.base_url}/api/v1/users/self/profile"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    data = res.json()
                    return {
                        "connected": True,
                        "user_id": data.get("id"),
                        "name": data.get("name"),
                        "primary_email": data.get("primary_email"),
                        "message": "Successfully authenticated with AWS Academy Canvas LMS API."
                    }
                else:
                    return {
                        "connected": False,
                        "status_code": res.status_code,
                        "message": f"Canvas API returned HTTP {res.status_code}: {res.text[:150]}",
                        "fallback_active": True
                    }
        except Exception as e:
            logger.warning(f"Canvas API test failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "message": "Connection to Canvas failed. Using local parsed HTML fallback.",
                "fallback_active": True
            }

    async def fetch_course_modules(self, course_id: str = "183194") -> List[Dict[str, Any]]:
        """Fetch all modules and nested items via read-only REST API."""
        if not self.api_token:
            logger.info("Canvas API token not set. Returning empty list (fallback mode active).")
            return []

        url = f"{self.base_url}/api/v1/courses/{course_id}/modules?include[]=items&include[]=content_details"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    return res.json()
                else:
                    logger.error(f"Canvas modules API returned {res.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Failed to fetch Canvas modules: {e}")
            return []

    async def fetch_assignments(self, course_id: str = "183194") -> List[Dict[str, Any]]:
        """Fetch course assignments and descriptions (read-only)."""
        if not self.api_token:
            return []
        url = f"{self.base_url}/api/v1/courses/{course_id}/assignments"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    return res.json()
                return []
        except Exception as e:
            logger.error(f"Failed to fetch assignments: {e}")
            return []

canvas_service = CanvasIntegrationService()
