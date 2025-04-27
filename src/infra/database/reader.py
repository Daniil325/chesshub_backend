from dataclasses import asdict
from datetime import datetime
from typing import Any

from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.article.entities import Article, Category, Tag
from src.infra.database.filters import SqlAlchemyBuilder
from src.infra.database.models.base import article_table, category_table, tag_table


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
        print(item)
        return item


class ArticleReader(BaseReader):
    stmt = select(Article, Category).join(Category)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, article_table, Article)

    @staticmethod
    def parse_item(item):
        if item:
            article_dict = asdict(item[0])
            article_dict["category_name"] = item[1].name
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
        print("ddddd", item)
        return None
        
    async def fetch_list_by_article(self, page, per_page, filter, order): ...


class CategoryReader(BaseReader):
    stmt = select(Category)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, category_table, Category)


class TagReader(BaseReader):
    stmt = select(Tag)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, tag_table, Tag)
