import pytest

from src.application.article.article_tag import CreateArticleTagCommand, CreateArticleTagDto
from src.infra.database.sqla_repo import ArticleTagRepo


@pytest.mark.unit
async def test_create_article_tag(mocker):
    article_tag_repo = mocker.AsyncMock(spec=ArticleTagRepo)
    article_tag_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateArticleTagCommand(article_tag_repo)

    result = await sut(CreateArticleTagDto("NEW-ID", "NEW_ID_2"))

    assert result == ("NEW-ID", "NEW_ID_2")
