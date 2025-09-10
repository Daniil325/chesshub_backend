from fastapi import APIRouter

router = APIRouter(tags=["integrations"])


@router.get("/integrations/lichess")
async def get_lichess_info(lichess_username: str):
    return {"bullet": None, "blitz": 1725, "rapid": None, "classical": None}


@router.get("/integrations/chesscom")
async def get_chesscom_info(chesscom_username: str):
    return {"chess_bullet": 3184, "chess_blitz": 3343, "chess_rapid": 2942}
