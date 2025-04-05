import pytest

from src.application.article.article_reaction import (
    CreateArticleReactionDto,
    CreateArticleReactionCommand,
    UpdateArticleReactionCommand,
    UpdateArticleReactionDto,
    DeleteArticleReactionCommand,
)
from src.domain.article.protocols import ArticleReactionRepo
from src.domain.article.entities import ArticleReaction, Reaction


@pytest.mark.unit
async def test_create_article_reaction(mocker):
    article_reaction_repo = mocker.AsyncMock(spec=ArticleReactionRepo)
    article_reaction_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateArticleReactionCommand(article_reaction_repo)

    result = await sut(
        CreateArticleReactionDto("сиськи", "безумный эффект манделлы в тачках")
    )

    assert result == "NEW-ID"


@pytest.mark.unit
async def test_update_article_reaction(mocker):
    article_reaction_repo = mocker.AsyncMock(spec=ArticleReactionRepo)
    existing_reaction = ArticleReaction.create("пэнис", "брейкданс", Reaction.LIKE)
    article_reaction_repo.get.return_value = existing_reaction

    sut = UpdateArticleReactionCommand(article_reaction_repo)

    await sut(UpdateArticleReactionDto("пэнис", Reaction.DISLIKE))

    assert existing_reaction.reaction == Reaction.DISLIKE


@pytest.mark.unit
async def test_delete_article_reaction(mocker):
    article_tag_repo = mocker.AsyncMock(spec=ArticleReactionRepo)

    sut = DeleteArticleReactionCommand(article_tag_repo)

    result = await sut("пэнис")

    assert result is None
