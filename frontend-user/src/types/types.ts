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
