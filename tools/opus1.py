import asyncio
from miniopy_async import Minio, S3Error

client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False  # http for False, https for True
)


async def main():
    url = await client.list_objects("content-images", prefix="aaa")
    print('url:', url)


asyncio.run(main())