from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PlayerStatus(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    LOBBY_WAITING = "LOBBY WAITING"
    LOBBY_READY = "LOBBY READY"
    PLAYING = "PLAYING"

class GameStatus(str, Enum):
    NOT_STARTED = "NOT STARTED"
    ROUND_ENDED = "ROUND ENDED"
    IN_PROGRESS = "ROUND IN PROGRESS"
    DEALING = "DEALING"

class PlayerState(BaseModel):
    status: PlayerStatus
    hand: list
    score: int

class GameState(BaseModel):
    status: GameStatus
    turn: int
    players: dict[int, PlayerState]

class Orientation(BaseModel):
    w: float
    x: float
    y: float
    z: float
    
class Position(BaseModel):
    x: float
    y: float
    z: float

    def __add__(self, other: "Position") -> "Position":
        return Position(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __mul__(self, number: int) -> "Position":
        return Position(
            x=self.x * number,
            y=self.y * number,
            z=self.z * number,
        )

class Pose(BaseModel):
    orientation: Orientation
    position: Position
    
class LogSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class LogItem(BaseModel):
    time: datetime = datetime.now()
    type: LogSeverity
    message: str
    
class Configuration(BaseModel):
    deck: Pose
    offsets: dict[str, Position]