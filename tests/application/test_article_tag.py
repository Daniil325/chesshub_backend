import pytest

from src.application.article.article_tag import (
    CreateArticleTagCommand,
    CreateArticleTagDto,
    UpdateArticleTagDto,
    UpdateArticleTagCommand,
    DeleteArticleTagCommand,
)
from src.domain.article.protocols import ArticleTagRepo
from src.domain.article.entities import ArticleTag


@pytest.mark.unit
async def test_create_article_tag(mocker):
    article_tag_repo = mocker.AsyncMock(spec=ArticleTagRepo)
    article_tag_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateArticleTagCommand(article_tag_repo)

    result = await sut(CreateArticleTagDto("NEW-ID", "NEW_ID_2"))

    assert result == ["NEW-ID", "NEW_ID_2"]


@pytest.mark.unit
async def test_update_article_tag(mocker):
    article_tag_repo = mocker.AsyncMock(spec=ArticleTagRepo)

    article_tag = ArticleTag.create("где б я не был", "там сороквторые")

    article_tag_repo.get.return_value = article_tag

    sut = UpdateArticleTagCommand(article_tag_repo)

    result = await sut(
        UpdateArticleTagDto(
            old_tag_id="где б я не был",
            old_article_id="там сороквторые",
            new_tag_id="где б вы не были",
            new_article_id="вы всегда вторые",
        )
    )

    assert result == ["где б вы не были", "вы всегда вторые"]


@pytest.mark.unit
async def test_delete_article_tag(mocker):
    article_tag_repo = mocker.AsyncMock(spec=ArticleTagRepo)

    sut = DeleteArticleTagCommand(article_tag_repo)

    result = await sut("где б я не был", "там сороквторые")

    assert result == ["где б я не был", "там сороквторые"]
