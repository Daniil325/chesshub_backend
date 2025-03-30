import pytest

from src.domain.article.entities import Tag
from src.application.article.tag import (
    CreateTagCommand,
    CreateTagDto,
    DeleteTagCommand,
    UpdateTagCommand,
    UpdateTagDto,
)
from src.infra.database.sqla_repo import TagRepo


@pytest.mark.unit
async def test_create_tag(mocker):
    tag_repo = mocker.AsyncMock(spec=TagRepo)
    tag_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateTagCommand(tag_repo)

    result = await sut(CreateTagDto("goooool"))

    assert result == "NEW-ID"
    entity = tag_repo.add.call_args_list[0][0][0]
    assert isinstance(entity, Tag)


@pytest.mark.unit
async def test_update_tag(mocker):
    tag_repo = mocker.AsyncMock(spec=TagRepo)
    tag = Tag.create("TAG_ID", "GOOOOOOOOOOL")
    tag_repo.get.return_value = tag

    sut = UpdateTagCommand(tag_repo)

    await sut(UpdateTagDto("TAG_ID", "HOHLIIIIII"))

    assert tag.name == "HOHLIIIIII"
    tag_repo.get.assert_awaited_with("TAG_ID")


@pytest.mark.unit
async def test_delete_tag(mocker):
    tag_repo = mocker.AsyncMock(spec=TagRepo)

    sut = DeleteTagCommand(tag_repo)

    res = await sut("TAG_ID")

    assert res == "TAG_ID"
