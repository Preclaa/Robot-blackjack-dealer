<script setup lang="ts">
import { GameStatus } from '@/types/types'

import { gameStateStore } from '@/stores/gamestate'
const game = gameStateStore()

import axios from 'axios'
import { endpoint } from '@/utils/api'

const startGame = () => {
    axios
        .post(endpoint(`/state/start`))
        .then((response) => {
            console.log('Game start success:', response)
        })
        .catch((error) => {
            console.error('Game start error:', error)
        })
}

const stopGame = () => {
    axios
        .post(endpoint(`/state/stop`))
        .then((response) => {
            console.log('Stop game success:', response)
        })
        .catch((error) => {
            console.error('Stop game error:', error)
        })
}

const newRound = () => {
    axios
        .post(endpoint(`/state/new_round`))
        .then((response) => {
            console.log('New round success:', response)
        })
        .catch((error) => {
            console.error('New round error:', error)
        })
}

const setFlip = (flip: boolean) => {
    axios
        .put(endpoint(`/state/flip/${flip}`))
        .then((response) => {
            console.log('Flip success:', response)
        })
        .catch((error) => {
            console.error('Flip error:', error)
        })
}

const setSimulation = (simulation: boolean) => {
    axios
        .put(endpoint(`/state/simulation/${simulation}`))
        .then((response) => {
            console.log('Simulation success:', response)
        })
        .catch((error) => {
            console.error('Simulation error:', error)
        })
}

</script>

<template>
    <div class="text-center small text-muted">{{ game.gameState.status }}</div>
    <button class="btn btn-success w-100 mt-2" @click="() => startGame()" v-if="game.gameState.status == GameStatus.NOT_STARTED">
        START GAME
    </button>
    <button class="btn btn-danger w-100 mt-2" @click="() => stopGame()" v-if="game.gameState.status != GameStatus.NOT_STARTED">
        STOP GAME
    </button>
    <button class="btn btn-primary w-100 mt-2" @click="() => newRound()" v-if="game.gameState.status == GameStatus.IN_PROGRESS">
        NEW ROUND
    </button>

    <div class="btn-group btn-group-toggle mt-3 w-100" data-toggle="buttons">
        <label class="btn btn-secondary" @click="setFlip(false)">
            <input type="radio" name="flip" id="flipoff" autocomplete="off" checked> FLIP OFF
        </label>
        <label class="btn btn-secondary" @click="setFlip(true)">
            <input type="radio" name="flip" id="flipon" autocomplete="off"> FLIP ON
        </label>
    </div>

    <div class="btn-group btn-group-toggle mt-3 w-100" data-toggle="buttons">
        <label class="btn btn-secondary" @click="setSimulation(false)">
            <input type="radio" name="sim" id="simoff" autocomplete="off" checked> LAB
        </label>
        <label class="btn btn-secondary" @click="setSimulation(true)">
            <input type="radio" name="sim" id="simon" autocomplete="off"> SIM
        </label>
    </div>
</template>