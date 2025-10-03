from dataclasses import asdict, dataclass

from src.domain.course.entities import Question
from src.domain.course.protocols import QuestionRepo


@dataclass
class CreateQuestionDto:
    name: str
    test_id: str


@dataclass
class CreateQuestionCommand:
    question_repo: QuestionRepo

    async def __call__(self, dto: CreateQuestionDto) -> str:
        identity = self.question_repo.new_id()
        question = Question.create(identity, dto.name, dto.test_id)
        await self.question_repo.add(question)
        return identity
    

@dataclass
class UpdateQuestionDto:
    id: str
    name: str


@dataclass
class UpdateQuestionCommand:
    question_repo: QuestionRepo

    async def __call__(self, dto: UpdateQuestionDto) -> None:
        question = await self.question_repo.get(dto.id)
        question.name = dto.name
        await self.question_repo.update(dto.id, asdict(dto))


@dataclass
class DeleteQuestionCommand:
    question_repo: QuestionRepo

    async def __call__(self, id: str) -> str:
        await self.question_repo.delete(id)
        return id
