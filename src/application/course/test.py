from dataclasses import asdict, dataclass


from src.domain.course.entities import Test
from src.domain.course.protocols import TestRepo


@dataclass
class TestDto:
    name: str
    min_score: int = 0
    time_limit: int = 0


@dataclass
class CreateTestCommand:
    test_repo: TestRepo

    async def __call__(self, dto: TestDto) -> str:
        identity = self.test_repo.new_id()
        test = Test.create(identity, dto.name, dto.min_score, dto.time_limit)
        await self.test_repo.add(test)
        return identity
    

@dataclass
class UpdateTestDto(TestDto):
    id: str
    

@dataclass
class UpdateTestCommand:
    test_repo: TestRepo

    async def __call__(self, dto: UpdateTestDto) -> None:
        test = await self.test_repo.get(dto.id)
        test.name = dto.name
        test.min_score = dto.min_score
        test.time_limit = dto.time_limit
        await self.test_repo.update(dto.id, asdict(test))


@dataclass
class DeleteTestCommand:
    test_repo: TestRepo

    async def __call__(self, id: str) -> str:
        await self.test_repo.delete(id)
        return id
