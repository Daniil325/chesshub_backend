import asyncio
from api import Lichess, Chesscom

async def main() -> None:
    username = Lichess("daniil325")
    json_result = await username.json_result()
    json_parse = await username.parse()
    print(json_result)

    username2 = Chesscom("bcurtis")
    json_result2 = await username2.json_result()
    json_parse2 = await username2.parse()
    print(json_result2)

asyncio.run(main())