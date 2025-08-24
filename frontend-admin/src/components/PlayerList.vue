<script setup lang="ts">
import axios from 'axios'

import { endpoint, websocket } from '@/utils/api'
import { PlayerStatus } from '@/types/types'
import { gameStateStore } from '@/stores/gamestate'
const game = gameStateStore()

const ws_game = websocket('/ws_player/0')

ws_game.onopen = () => {
    console.log('WebSocket (dealer) connection established')
}
ws_game.onmessage = (event) => {
    console.log('Message from server:', event.data)
    const result = JSON.parse(event.data)
    game.setGameState(result)
}
ws_game.onerror = (error) => {
    console.error('WebSocket (dealer) error:', error)
}
ws_game.onclose = () => {
    console.log('WebSocket (dealer) connection closed')
}

const disconnectPlayer = (player: number) => {
    axios
        .post(endpoint(`/players/disconnect/${player}`))
        .then(() => {
            console.log('Player disconnected')
        })
        .catch((error) => {
            console.error('Disconnect error:', error)
        })
}

</script>

<template>
    <div v-if="Object.keys(game.gameState.players).length > 0">
        <div class="card my-2">
            <div class="card-header fs-5">
                Dealer
            </div>
            <div v-if="game.gameState.players[0].status != PlayerStatus.LOBBY_WAITING" class="card-body d-flex justify-content-between px-3 py-2">
                <div class="d-flex align-items-center card-text">
                    <div v-for="card in game.gameState.players[0].hand" :key="card" class="suit" :class="card.slice(-1)">
                        {{ card }}
                    </div>
                </div>
                <span class="fs-3 text-center">{{ game.gameState.players[0].score }}</span>
            </div>
        </div>

        <div v-for="(player, index) in Object.values(game.gameState.players).slice(1)" :key="index">
            <div class="card my-2" :class="player.status == PlayerStatus.DISCONNECTED ? 'opacity-25' : ''">
                <div class="card-header d-flex justify-content-between">
                    <div class="fs-5">
                        <span v-if="player.status == PlayerStatus.PLAYING">
                            <i class="bi bi-arrow-right text-primary" v-if="game.gameState.turn == index + 1"></i>
                        </span>

                        Player {{ index + 1 }}
                        <small class="text-muted">
                            ({{ player.status }})
                        </small>
                    </div>
                    <div v-if="player.status != PlayerStatus.DISCONNECTED">
                        <button class="btn btn-outline-danger btn-sm" @click="() => disconnectPlayer(index + 1)" title="Disconnect">
                            <i class="bi bi-box-arrow-right"></i>
                        </button>
                    </div>
                </div>
                <div v-if="player.status == PlayerStatus.PLAYING || (player.status == PlayerStatus.LOBBY_WAITING && player.score > 0)" class="card-body d-flex justify-content-between px-3 py-2">
                    <div class="d-flex align-items-center card-text">
                        <div v-for="card in player.hand" class="suit" :key="card" :class="card.slice(-1)">
                            {{ card }}
                        </div>
                    </div>
                    <span class="fs-3 text-center">{{ player.score }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
