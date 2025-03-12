import httpx, asyncio
from api_dataclasses import Lichess, Chesscom

class ApiUse():

    def __init__(self, username: str) -> None:
        self._username = username

    def url_lichess(self) -> str:
        return f"https://lichess.org/api/user/{self._username}"

    def url_chesscom(self) -> str:
        return f"https://api.chess.com/pub/player/{self._username}/stats"

    async def urls_check(self, url: str) -> None:
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
            except httpx.HTTPStatusError as exc:
                print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    
    @staticmethod
    def lichess_result_parsing(json_dict: dict) -> Lichess:
        pars = {
            "bullet": json_dict.get("perfs", None).get("bullet", None),
            "blitz": json_dict.get("perfs", None).get("blitz", None),
            "rapid": json_dict.get("perfs", None).get("rapid", None),
            "classical": json_dict.get("perfs", None).get("classical", None),
        }
        return Lichess(**pars)
    
    @staticmethod
    def chesscom_result_parsing(json_dict: dict) -> Chesscom:
        pars = {
            "chess_blitz": json_dict.get("chess_blitz", None),
            "chess_rapid": json_dict.get("chess_rapid", None),
            "chess_bullet": json_dict.get("chess_bullet", None)
        }
        return Chesscom(**pars)

async def main() -> None:
    username = ApiUse('daniil325')
    url_lich = username.url_lichess()
    url_chcom = username.url_chesscom()
    result_lichess = await username.urls_check(url_lich)
    result_chesscom = await username.urls_check(url_chcom)
    test_lichess = username.lichess_result_parsing(result_lichess)
    test_chesscom = username.chesscom_result_parsing(result_chesscom)
    print(test_lichess)
    print("-" * 100)
    print(test_chesscom)

asyncio.run(main())




















