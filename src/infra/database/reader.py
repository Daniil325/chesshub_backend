from dataclasses import asdict
from itertools import groupby
from uuid import UUID

from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.entities import User
from src.domain.course.entities import Answer, Course, Lesson, Question, Test
from src.domain.article.entities import Article, Category, Tag
from src.infra.database.filters import SqlAlchemyBuilder
from src.infra.database.models.base import (
    article_table,
    category_table,
    tag_table,
    course_table,
    lesson_table,
    test_table,
    user_table
)


class BaseReader:
    stmt = None

    def __init__(self, session: AsyncSession, table: Table, model) -> None:
        self.session = session
        self.table = table
        self.model = model
        self.filter_builder = SqlAlchemyBuilder(self.table, self.stmt)

    async def fetch_list(self, page: int, per_page: int, filter: str, order_by: str):
        self.stmt = self.filter_builder(filter, order_by)
        self.stmt = self.stmt.limit(per_page).offset(page * per_page)
        items = (await self.session.execute(self.stmt)).scalars().all()
        return items

    async def fetch_by_id(self, id: str):
        stmt = select(self.model).where(self.model.id == id)
        item = (await self.session.execute(stmt)).scalar_one_or_none()
        return item


class ArticleReader(BaseReader):
    stmt = select(Article, Category, User).join(Category).join(User)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, article_table, Article)

    @staticmethod
    def parse_item(item):
        if item:
            article_dict = asdict(item[0])
            article_dict["category_name"] = item[1].name
            article_dict["username"] = item[2].username
            return article_dict
        return item

    async def fetch_list(
        self, page: int, per_page: int, filter: str, order_by: str
    ) -> list[Article]:
        self.stmt = self.filter_builder(filter, order_by)
        self.stmt = self.stmt.limit(per_page).offset(page * per_page)
        items = (await self.session.execute(self.stmt)).all()
        result = [self.parse_item(item) for item in items]
        return result

    async def fetch_by_id(self, id: str):
        self.stmt = self.stmt.where(Article.id == id)
        item = (await self.session.execute(self.stmt)).all()
        if item:
            return self.parse_item(item[0])
        return None

    async def fetch_list_by_article(self, page, per_page, filter, order): ...


class CourseReader(BaseReader):
    stmt = select(Course, User).join(User)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, course_table, Course)
        
    @staticmethod
    def parse_item(item):
        course_dict = asdict(item[0])
        course_dict["author_username"] = item[1].username
        return course_dict
    
    @staticmethod
    def parse_item_detail(items):
        course = asdict(items[0][0])
        lessons = []
        for it in items:
            tmp = it[1]
            lessons.append(asdict(tmp))
        course["lessons"] = lessons
        return course
        

    async def fetch_list(
        self,
        page: int,
        per_page: int,
        filter: str,
        order_by: str,
    ) -> list[Course]:
        self.stmt = self.filter_builder(filter, order_by)
        self.stmt = self.stmt.limit(per_page).offset(page * per_page)
        items = (await self.session.execute(self.stmt)).all()
        result = [self.parse_item(item) for item in items]
        return result

    async def fetch_by_id(self, id: UUID):
        self.stmt = select(Course, Lesson).join(Lesson).where(Course.id == id)
        result = (await self.session.execute(self.stmt)).all()
        print(result)
        return self.parse_item_detail(result)


class LessonReader(BaseReader):
    stmt = select(Lesson)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, lesson_table, Course)

    async def fetch_list(
        self,
        page: int,
        per_page: int,
        filter: str,
        order_by: str,
    ) -> list[Lesson]:
        self.stmt = self.filter_builder(filter, order_by)
        items = (await self.session.execute(self.stmt)).scalars().all()
        # result = [self.parse_item(item) for item in items]
        return items

    async def fetch_by_id(self, id: UUID):
        self.stmt = select(Lesson, Test).join(Test).where(Lesson.id == id)
        result = (await self.session.execute(self.stmt)).all()
        return result


class TestReader(BaseReader):
    stmt = select(Test)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, test_table, Test)

    @staticmethod
    def grouper(item):
        return item["question_id"]

    def parse_item(self, items):
        questions = []
        answers = []
        for i in items:
            if asdict(i[1]) not in questions:
                questions.append(asdict(i[1]))
            if asdict(i[2]) not in answers:
                answers.append(asdict(i[2]))

        answers = sorted(answers, key=self.grouper)
        for key, group_items in groupby(answers, key=self.grouper):
            for question in questions:
                if question["id"] == key:
                    question["answers"] = [i for i in group_items]

        result = asdict(items[0][0])
        result["questions"] = questions
        return result

    async def fetch_by_id(self, id: UUID):
        stmt = (
            select(Test, Question, Answer)
            .filter(Question.test_id == Test.id)
            .filter(Answer.question_id == Question.id)
            .where(Test.id == id)
        )
        items = (await self.session.execute(stmt)).all()
        result = self.parse_item(items)
        return result


class CategoryReader(BaseReader):
    stmt = select(Category)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, category_table, Category)


class TagReader(BaseReader):
    stmt = select(Tag)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, tag_table, Tag)
        
        
class UserReader(BaseReader):
    stmt = select(User)
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, user_table, User)
        
    @staticmethod
    def parse_item(items):
        user_dict = asdict(items[0][0])
        
        articles = []
        courses = []
        
        for i in items:
            article_dict = asdict(i[1])
            course_dict = asdict(i[2])
            if article_dict not in articles:
                articles.append(article_dict)
            if course_dict not in courses:
                courses.append(course_dict)
        user_dict["articles"] = articles
        user_dict["courses"] = courses
        return user_dict

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User, Article, Course).join(Article).join(Course).where(User.username == username)
        user = (await self.session.execute(stmt)).all()
        return self.parse_item(user)