import pytest

from src.application.article.tag import CreateTagCommand, CreateTagDto
from src.infra.database.sqla_repo import TagRepo


@pytest.mark.unit
async def test_create_tag(mocker):
    tag_repo = mocker.AsyncMock(spec=TagRepo)
    tag_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateTagCommand(tag_repo)

    result = await sut(CreateTagDto("goooool"))

    assert result == "NEW-ID"
