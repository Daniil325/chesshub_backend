from dataclasses import dataclass

from src.domain.article.entities import Tag
from src.infra.database.sqla_repo import TagRepo


@dataclass(frozen=True)
class CreateTagDto:
    name: str


@dataclass
class CreateTagCommand:
    tag_repo: TagRepo

    async def __call__(self, dto: CreateTagDto) -> str:
        identity = self.tag_repo.new_id()
        tag = Tag.create(identity, dto.name)
        await self.tag_repo.create(tag)
        return identity
