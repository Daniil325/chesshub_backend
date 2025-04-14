import pytest

from infra.protocols import S3Storage
from src.application.article.article import CreateArticleCommand, CreateArticleDto
from src.domain.article.protocols import ArticleRepo
from src.domain.article.entities import Article


@pytest.mark.unit
async def test_create_article(mocker):
    article_repo = mocker.AsyncMock(spec=ArticleRepo)
    article_repo.new_id = mocker.Mock(return_value="NEW-ID")
    image_storage = mocker.AsyncMock(spec=S3Storage)

    sut = CreateArticleCommand(article_repo, image_storage)

    result = await sut(CreateArticleDto("TITLE", {"jjjj": "jjjlkj", "test": "aaaa"},  "CAT_ID", None))

    assert result == "NEW-ID"
    entity = article_repo.add.call_args_list[0][0][0]
    assert isinstance(entity, Article)
    assert entity.content == {"jjjj": "jjjlkj", "test": "aaaa"}
    assert entity.preview is None
