from dataclasses import asdict, dataclass

from src.domain.article.entities import Tag
from src.domain.article.protocols import TagRepo


@dataclass(frozen=True)
class CreateTagDto:
    name: str


@dataclass
class CreateTagCommand:
    tag_repo: TagRepo

    async def __call__(self, dto: CreateTagDto) -> str:
        identity = self.tag_repo.new_id()
        tag = Tag.create(identity, dto.name)
        await self.tag_repo.add(tag)
        return identity


@dataclass(frozen=True)
class UpdateTagDto:
    tag_id: str
    name: str


@dataclass
class UpdateTagCommand:
    tag_repo: TagRepo

    async def __call__(self, dto: UpdateTagDto) -> str:
        tag = await self.tag_repo.get(dto.tag_id)
        tag.name = dto.name
        await self.tag_repo.update(dto.tag_id, asdict(tag))


@dataclass
class DeleteTagCommand:
    tag_repo: TagRepo

    async def __call__(self, content_id: str) -> None:
        await self.tag_repo.delete(content_id)
        return content_id
