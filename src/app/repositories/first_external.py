from abc import ABC, abstractmethod

from app.core.config import settings
from app.repositories.base import HTTPRepository


class AbstractFirstExternalRepository(ABC):
    @abstractmethod
    async def get_description_by_name(self, name: str) -> str:
        pass


class HTTPFirstExternalRepository(AbstractFirstExternalRepository, HTTPRepository):
    def __init__(self):
        super().__init__(host=settings.first_external_host)

    async def get_description_by_name(self, name: str) -> str:
        result = await self.get("/path/to/route", json={"name": name})
        return result["description"]
