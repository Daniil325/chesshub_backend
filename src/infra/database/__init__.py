from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.protocols import UserRepo
from src.infra.database.repositories.user import SqlUserRepo
from src.domain.article.protocols import (
    ArticleReactionRepo,
    ArticleRepo,
    ArticleTagRepo,
    CategoryRepo,
    TagRepo,
)
from src.domain.course.protocols import (
    AnswerRepo,
    CourseRepo,
    LessonRepo,
    QuestionRepo,
    TestRepo,
)
from src.infra.database.reader import (
    ArticleReader,
    CategoryReader,
    CourseReader,
    LessonReader,
    TagReader,
    TestReader,
    UserReader,
)
from src.infra.database.repositories.article import (
    SqlArticleReactionRepo,
    SqlArticleRepo,
    SqlArticleTagRepo,
    SqlCategoryRepo,
    SqlTagRepo,
)
from src.infra.database.repositories.course import (
    SqlAnswerRepo,
    SqlCourseRepo,
    SqlLessonRepo,
    SqlQuestionRepo,
    SqlTestRepo,
)
from src.infra.database.session import DBSession


class DBSessionProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    @provide
    def get_db(self) -> DBSession:
        return DBSession(self.settings)

    @provide
    async def get_session(self, db: DBSession) -> AsyncIterable[AsyncSession]:
        async with db.sessionmaker() as session:
            yield session


class SqlProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    def get_user_repo(self, session: AsyncSession) -> UserRepo:
        return SqlUserRepo(session)

    @provide
    def get_content_repo(self, session: AsyncSession) -> TagRepo:
        return SqlTagRepo(session)

    @provide
    def get_article_repo(self, session: AsyncSession) -> ArticleRepo:
        return SqlArticleRepo(session)

    @provide
    def get_category_repo(self, session: AsyncSession) -> CategoryRepo:
        return SqlCategoryRepo(session)

    @provide
    def get_article_tag_repo(self, session: AsyncSession) -> ArticleTagRepo:
        return SqlArticleTagRepo(session)

    @provide
    def get_article_reaction_repo(self, session: AsyncSession) -> ArticleReactionRepo:
        return SqlArticleReactionRepo(session)

    @provide
    def get_course_repo(self, session: AsyncSession) -> CourseRepo:
        return SqlCourseRepo(session)

    @provide
    def get_test_repo(self, session: AsyncSession) -> TestRepo:
        return SqlTestRepo(session)

    @provide
    def get_lesson_repo(self, session: AsyncSession) -> LessonRepo:
        return SqlLessonRepo(session)

    @provide
    def get_question_repo(self, session: AsyncSession) -> QuestionRepo:
        return SqlQuestionRepo(session)

    @provide
    def get_answer_repo(self, session: AsyncSession) -> AnswerRepo:
        return SqlAnswerRepo(session)


class ReadersProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    def get_article_reader(self, session: AsyncSession) -> ArticleReader:
        return ArticleReader(session)

    @provide
    def get_category_reader(self, session: AsyncSession) -> CategoryReader:
        return CategoryReader(session)

    @provide
    def get_tag_reader(self, session: AsyncSession) -> TagReader:
        return TagReader(session)

    @provide
    def get_course_reader(self, session: AsyncSession) -> CourseReader:
        return CourseReader(session)

    @provide
    def get_lesson_reader(self, session: AsyncSession) -> LessonReader:
        return LessonReader(session)

    @provide
    def get_test_reader(self, session: AsyncSession) -> TestReader:
        return TestReader(session)
    
    @provide
    def get_user_reader(self, session: AsyncSession) -> UserReader:
        return UserReader(session)
