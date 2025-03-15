from abc import ABC, abstractmethod
import httpx

class ApiUse(ABC):
    
    def __init__(self, username: str) -> None:
        self._username = username

    async def urls_check(self, url: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
            except httpx.HTTPStatusError as exc:
                print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

    @abstractmethod
    async def parse(self):
        pass