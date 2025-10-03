from api_dataclasses import LichessData, ChesscomData
from api_baseclass import ApiUse


class Lichess(ApiUse):

    def __init__(self, username: str) -> None:
        super().__init__(username)
        self._api_url = f"https://lichess.org/api/user/{self._username}"
        self._keys = ["bullet", "blitz", "rapid", "classical"]
        self._json_parse = dict()

    async def json_result(self) -> dict:
        return await self.urls_check(self._api_url)

    async def parse(self) -> LichessData:
        json_dict = await self.json_result()
        for i in self._keys:
            self._json_parse[i] = (
                json_dict.get("perfs", dict()).get(i, dict()).get("rating", None)
            )
        return LichessData(**self._json_parse)


class Chesscom(ApiUse):

    def __init__(self, username: str) -> None:
        super().__init__(username)
        self._api_url = f"https://api.chess.com/pub/player/{self._username}/stats"
        self._keys = ["chess_blitz", "chess_rapid", "chess_bullet"]
        self._json_parse = dict()

    async def json_result(self) -> dict:
        return await self.urls_check(self._api_url)

    async def parse(self) -> ChesscomData:
        json_dict = await self.json_result()
        for i in self._keys:
            self._json_parse[i] = (
                json_dict.get(i, dict()).get("last", dict()).get("rating", None)
            )
        return ChesscomData(**self._json_parse)
