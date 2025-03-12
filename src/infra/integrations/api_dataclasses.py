from dataclasses import dataclass

@dataclass
class Lichess():
    bullet: dict
    blitz: dict 
    rapid: dict
    classical: dict

@dataclass
class Chesscom():
    chess_blitz: dict
    chess_rapid: dict
    chess_bullet: dict