export enum PlayerStatus {
    DISCONNECTED = "DISCONNECTED",
    LOBBY_WAITING = "LOBBY WAITING",
    LOBBY_READY = "LOBBY READY",
    PLAYING = "PLAYING",
}

export enum GameStatus {
    NOT_STARTED = "NOT STARTED",
    ROUND_ENDED = "ROUND ENDED",
    IN_PROGRESS = "ROUND IN PROGRESS",
    DEALING = "DEALING"
}

export interface PlayerState {
    hand: string[];
    score: number;
    status: PlayerStatus;
}

export interface GameState {
    status: GameStatus;
    turn: number;
    players: Record<string, PlayerState>;
}

export interface LogMessage {
    type: string;
    time: string;
    message: string;
}

export interface Position {
    x: number;
    y: number;
    z: number;
}

export interface Orientation {
    w: number;
    x: number;
    y: number;
    z: number;
}

export interface Pose {
    orientation: Orientation;
    position: Position;
}
