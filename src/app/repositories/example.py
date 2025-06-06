from abc import ABC, abstractmethod

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter


class AbstractExampleRepository(ABC):
    @abstractmethod
    async def get_all_examples(self, filter: ExamplesFilter) -> list[Example]:
        pass

    @abstractmethod
    async def create_example(self, name: str, description: str) -> Example:
        pass

    @abstractmethod
    async def commit(self):
        pass


class SQLExampleRepository(AbstractExampleRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_examples(self, filter: ExamplesFilter) -> list[Example]:
        filters = []
        if filter.example_ids is not None:
            filters.append(models.Examples.id.in_(filter.example_ids))
        if filter.created_before is not None:
            filters.append(models.Examples.created_at <= filter.created_before)
        if filter.created_after is not None:
            filters.append(models.Examples.created_at >= filter.created_after)

        q = select(
            models.Examples.id,
            models.Examples.name,
            models.Examples.description,
            models.Examples.created_at,
            models.Examples.updated_at,
        ).where(and_(*filters))
        raw_result = await self.db_session.execute(q)

        data = []
        for example in raw_result.all():
            data.append(
                Example(
                    id=example.id,
                    name=example.name,
                    description=example.description,
                    created_at=example.created_at,
                    updated_at=example.updated_at,
                )
            )
        return data

    async def create_example(self, name: str, description: str) -> Example:
        raw_object = models.Examples(name=name, description=description)
        self.db_session.add(raw_object)
        await self.db_session.flush()
        return Example(
            id=raw_object.id,
            name=raw_object.name,
            description=raw_object.description,
            created_at=raw_object.created_at,
            updated_at=raw_object.updated_at,
        )

    async def commit(self):
        await self.db_session.commit()
