from dataclasses import dataclass


@dataclass
class LichessData:
    bullet: int | None = None
    blitz: int | None = None
    rapid: int | None = None
    classical: int | None = None


@dataclass
class ChesscomData:
    chess_blitz: int | None = None
    chess_rapid: int | None = None
    chess_bullet: int | None = None
