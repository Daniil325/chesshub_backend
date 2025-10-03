from dataclasses import asdict, dataclass

from src.domain.course.entities import Answer
from src.domain.course.protocols import AnswerRepo


@dataclass
class CreateAnswerDto:
    text: str
    question_id: str
    is_right: bool


@dataclass
class CreateAnswerCommand:
    answer_repo: AnswerRepo

    async def __call__(self, dto: CreateAnswerDto) -> str:
        identity = self.answer_repo.new_id()
        answer = Answer.create(identity, dto.text, dto.question_id, dto.is_right)
        await self.answer_repo.add(answer)
        return identity
    

@dataclass
class UpdateAnswerDto:
    id: str
    text: str
    is_right: bool


@dataclass
class UpdateAnswerCommand:
    answer_repo: AnswerRepo

    async def __call__(self, dto: UpdateAnswerDto) -> None:
        answer = await self.answer_repo.get(dto.id)
        answer.text = dto.text
        answer.is_right = dto.is_right
        await self.answer_repo.update(answer)


@dataclass
class DeleteAnswerCommand:
    answer_repo: AnswerRepo

    async def __call__(self, id: str) -> str:
        await self.answer_repo.delete(id)
        return id