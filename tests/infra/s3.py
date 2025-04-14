from datetime import datetime

import aiohttp
import pytest

from src.infra.s3.minio import MinioImageRepo, secure_filename, ImageDescr


@pytest.mark.unit
@pytest.mark.parametrize(
    "input, result",
    (
        ("1.png", "1.png"),
        ("../1.png", "1.png"),
        ("/1.png", "1.png"),
        ("./1.png", "1.png"),
    ),
)
def test_secure_filename(input, result):
    assert secure_filename(input) == result


@pytest.fixture()
async def storage(minio_settings, minio_client):
    async with aiohttp.ClientSession(trust_env=True) as session:
        yield MinioImageRepo(minio_settings, session)


@pytest.mark.integration
class TestS3ImageStorage:

    async def test_exists(self, storage):
        assert (await storage.exists("1.png")) is True

    async def test_not_exists(self, storage):
        assert (await storage.exists("penis.png")) is False

    async def test_create_new_id(self, storage):
        result = await storage.create_new_id("../three.jpg")
        assert result == "three.jpg"

    async def test_create_new_id_exists(self, storage):
        result = await storage.create_new_id("../1.png")
        assert result == "1-1.png"

    async def test_download(self, fixtures_path, storage):
        result = await storage.download("2.png")
        with (fixtures_path / "images" / "2.png").open("rb") as fd:
            assert result == fd.read()

    async def test_upload(self, fixtures_path, storage):
        with (fixtures_path / "photo.png").open("rb") as fd:
            content = fd.read()
            fd.seek(0)
            identity = await storage.upload("photo.png", fd)
        assert identity == "photo.png"
        uploaded = await storage.download(identity)
        assert uploaded == content

    async def test_get(self, storage):
        result = await storage.get("1.png")
        assert isinstance(result, ImageDescr)
        assert result.content_type == "image/png"
        assert result.url == "/media/article-images-test/1.png"
        assert result.height == 802
        assert result.width == 623
        assert result.size == 545801
        assert isinstance(result.created_at, datetime)

    async def test_list(self, storage):
        ls = [x async for x in storage.list("1")]
        print(ls)
        assert len(ls) == 1
        assert isinstance(ls[0], ImageDescr)
        assert ls[0].url == "/media/article-images-test/1.png"
