import pytest

from src.application.article.category import CreateCategoryCommand, CreateCategoryDto
from src.infra.database.sqla_repo import CategoryRepo


@pytest.mark.unit
async def test_create_category(mocker):
    category_repo = mocker.AsyncMock(spec=CategoryRepo)
    category_repo.new_id = mocker.Mock(return_value="NEW-ID")

    sut = CreateCategoryCommand(category_repo)

    result = await sut(CreateCategoryDto("йей"))

    assert result == "NEW-ID"
