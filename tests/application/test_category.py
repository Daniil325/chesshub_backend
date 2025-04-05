import pytest

from src.domain.article.entities import Category
from src.application.article.category import (
    CreateCategoryCommand,
    CreateCategoryDto,
    UpdateCategoryCommand,
    DeleteCategoryCommand,
    UpdateCategoryDto,
)
from src.domain.article.protocols import CategoryRepo


@pytest.mark.unit
async def test_create_category(mocker):
    category_repo = mocker.AsyncMock(spec=CategoryRepo)
    category_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateCategoryCommand(category_repo)

    result = await sut(CreateCategoryDto("йей"))

    assert result == "NEW-ID"
    entity = category_repo.add.call_args_list[0][0][0]
    assert isinstance(entity, Category)


@pytest.mark.unit
async def test_update_tag(mocker):
    category_repo = mocker.AsyncMock(spec=CategoryRepo)
    category = Category.create("посотри на стрижку", "нахуя мне кепка")
    category_repo.get.return_value = category

    sut = UpdateCategoryCommand(category_repo)

    await sut(UpdateCategoryDto("посотри на стрижку", "бигтести и бигмаков ночью заточил вчера"))

    assert category.name == "бигтести и бигмаков ночью заточил вчера"
    category_repo.get.assert_awaited_with("посотри на стрижку")


@pytest.mark.unit
async def test_delete_tag(mocker):
    category_repo = mocker.AsyncMock(spec=CategoryRepo)

    sut = DeleteCategoryCommand(category_repo)

    res = await sut("TAG_ID")

    assert res == "TAG_ID"
