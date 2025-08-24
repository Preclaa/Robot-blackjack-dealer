import { defineStore } from 'pinia'
import type { GameState } from '@/types/types'
import { GameStatus } from '@/types/types'

export const gameStateStore = defineStore('game', {
    state: (): { gameState: GameState } => ({
        gameState: {
            status: GameStatus.NOT_STARTED,
            turn: 0,
            players: {},
        },
    }),
    actions: {
        setGameState(newState: GameState) {
            this.gameState = newState
        },
    },
})