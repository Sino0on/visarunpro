import httpx
import logging
from typing import Optional, Any, Dict, List
from config import BACKEND_URL, API_SECRET_KEY

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = BACKEND_URL.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {API_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                if response.status_code == 204:
                    return dict()
                if response.content:
                    return response.json()
                return dict()
        except httpx.TimeoutException:
            logger.error(f"Timeout error on {method} {url}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} on {method} {url}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error on {method} {url}: {str(e)}")
            raise

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            return await self._request("GET", f"users/{user_id}/")
        except httpx.HTTPError:
            return None

    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return await self._request("POST", "users/", json=user_data)
        except httpx.HTTPError:
            return None

    async def get_destinations(self) -> List[Dict[str, Any]]:
        try:
            res = await self._request("GET", "destinations/")
            return res if res else []
        except httpx.HTTPError:
            return []

    async def get_schedule(self, destination_id: int) -> List[Dict[str, Any]]:
        try:
            res = await self._request("GET", "schedule/", params={"destination_id": destination_id})
            return res if res else []
        except httpx.HTTPError:
            return []

    async def create_booking(self, booking_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Let the exception bubble up to handle it in handler
        return await self._request("POST", "bookings/", json=booking_data)

api_client = APIClient()
