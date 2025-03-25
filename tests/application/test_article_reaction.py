import pytest

from src.application.article.article_reaction import CreateArticleReactionDto, CreateArticalReactionCommand
from src.infra.database.sqla_repo import ArticalReactionRepo


@pytest.mark.unit
async def test_create_article_reaction(mocker):
    article_reaction_repo = mocker.AsyncMock(spec=ArticalReactionRepo)
    article_reaction_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateArticalReactionCommand(article_reaction_repo)

    result = await sut(CreateArticleReactionDto("сиськи", "безумный эффект манделлы в тачках"))

    assert result == "NEW-ID"
