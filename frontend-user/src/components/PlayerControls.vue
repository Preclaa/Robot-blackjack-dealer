<script setup lang="ts">

import { ref, watch } from 'vue'

import type { GameState } from '@/types/types'
import { GameStatus, PlayerStatus } from '@/types/types'

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const API_URL = import.meta.env.VITE_API_WS_URL

const position = ref(Number(new URLSearchParams(window.location.search).get('position')) || 1);

const ws_game = ref<WebSocket | null>(null)
const connected = ref(false)
const position_occupied = ref(false)

const gameState = ref<GameState>({
  status: GameStatus.NOT_STARTED,
  turn: 0,
  players: {},
})


watch(ws_game, (ws_game_connected) => {
  if (ws_game_connected) {
    ws_game_connected.onopen = () => {
      connected.value = true
    }
    ws_game_connected.onmessage = (event) => {
      const result = JSON.parse(event.data)

      gameState.value = result;
    }
    ws_game_connected.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    ws_game_connected.onclose = (event) => {
      if (event.code === 1008) {
        position_occupied.value = true;
      }

      connected.value = false;
    }
  }
})

const connect = () => {
  if (position.value < 1 || position.value > 3) {
    position.value = 1;
  }
  position_occupied.value = false;
  ws_game.value = new WebSocket(`${API_URL}/ws_player/${position.value}`)
}

const disconnect = () => {
  if (ws_game.value) {
    ws_game.value.close()
    ws_game.value = null
    connected.value = false
  }
}

const hit = () => {
  const message = {
    player_id: position.value,
    action: 'hit',
  }
  if (ws_game.value) {
    ws_game.value.send(JSON.stringify(message))
  }
}

const stand = () => {
  const message = {
    player_id: position.value,
    action: 'stand',
  }
  if (ws_game.value) {
    ws_game.value.send(JSON.stringify(message))
  }
}

const ready = () => {
  const message = {
    player_id: position.value,
    action: 'ready',
  }
  if (ws_game.value) {
    ws_game.value.send(JSON.stringify(message))
  }
}

const getGameResultMessage = (): string => {
  const score = gameState.value.players[position.value].score;
  const scoreDealer = gameState.value.players[0].score;
  if (score > 21 || (score <= 21 && scoreDealer <= 21 && score < scoreDealer)) {
    return t("message.lose");
  } else if (score <= 21 && (scoreDealer > 21 || score > scoreDealer)) {
    return t("message.win");
  } else {
    return t("message.draw");
  }
};

const getResultClass = (): string => {
  const score = gameState.value.players[position.value].score;
  const scoreDealer = gameState.value.players[0].score;
  if (score > 21 || (score <= 21 && scoreDealer <= 21 && score < scoreDealer)) {
    return 'bg-danger';
  } else if (score <= 21 && (scoreDealer > 21 || score > scoreDealer)) {
    return 'bg-success';
  } else {
    return 'bg-secondary';
  }
};

</script>

<template>
  <div v-if="!connected" class="my-auto">
    <div class="btn-group mb-4 w-100" role="group" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" :checked="position === 1" @change="position = 1">
      <label class="btn btn-outline-primary" :class="{ active: position === 1 }" for="btnradio1">{{ $t("message.player") }} 1</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" :checked="position === 2" @change="position = 2">
      <label class="btn btn-outline-primary" :class="{ active: position === 2 }" for="btnradio2">{{ $t("message.player") }} 2</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" :checked="position === 3" @change="position = 3">
      <label class="btn btn-outline-primary" :class="{ active: position === 3 }" for="btnradio3">{{ $t("message.player") }} 3</label>
    </div>
    <div v-if="position_occupied" class="alert alert-danger text-center">
      {{ $t("message.position_occupied") }}
    </div>
    <button class="btn btn-lg fw-bold btn-primary w-100 custom-button" @click="() => connect()">
      {{ $t("message.connect") }}
    </button>
  </div>
  <div v-else class="d-flex flex-column my-auto">
    <div>
      <div class="card my-1">
        <div class="card-header text-center fs-4">
          Dealer
        </div>
        <div class="card-body d-flex justify-content-between">
          <div class="d-flex align-items-center card-text">
            <div v-for="(card, index) in gameState.players[0].hand" :key="index" class="suit" :class="card.slice(-1)">
              {{ card }}
            </div>
          </div>
          <div class="d-flex flex-column">
            <span class="text-center">{{ $t("message.score") }}</span>
            <span class="fs-1 text-center">{{ gameState.players[0].score }}</span>
          </div>
        </div>
      </div>

      <div class="card my-1">
        <div class="card-header text-center fs-4">
          {{ $t("message.player") }} {{ position }} - {{ $t("message.cards") }}
        </div>
        <div class="card-body d-flex justify-content-between">
          <div class="d-flex align-items-center card-text">
            <div v-for="(card, index) in gameState.players[position].hand" :key="index" class="suit" :class="card.slice(-1)">
              {{ card }}
            </div>
          </div>
          <div class="d-flex flex-column">
            <span class="text-center">{{ $t("message.score") }}</span>
            <span class="fs-1 text-center">{{ gameState.players[position].score }}</span>
          </div>
        </div>
        <div class="fs-5 text-center text-white py-3" v-if="gameState.status === GameStatus.ROUND_ENDED && gameState.players[position].score > 0" :class="getResultClass()">
          {{ getGameResultMessage() }}
        </div>
      </div>
    </div>

    <div class="fs-1 py-3 text-center fw-bold" :class="gameState.turn === position && gameState.status == GameStatus.IN_PROGRESS ? 'text-success' : ''">
      <span v-if="gameState.status == GameStatus.ROUND_ENDED || gameState.status == GameStatus.NOT_STARTED">
        {{ $t("message.waiting") }}
      </span>
      <span v-if="gameState.status == GameStatus.DEALING">
        {{ $t("message.dealing") }}
      </span>
      <span v-if="gameState.status == GameStatus.IN_PROGRESS && gameState.turn == position">
        {{ $t("message.turn_yours") }}
      </span>
      <span v-if="gameState.status == GameStatus.IN_PROGRESS && gameState.turn != position">
        {{ $t('message.turn_player', [gameState.turn]) }}
      </span>
    </div>
    <div class="d-flex justify-content-center" v-if="gameState.status == GameStatus.IN_PROGRESS && gameState.turn > 0">
      <button class="btn btn-primary fs-1 w-50 rounded-0 rounded-start custom-button" :disabled="gameState.turn != position" @click="hit">
        HIT
      </button>
      <button class="btn btn-secondary fs-1 w-50 rounded-0 rounded-end custom-button" :disabled="gameState.turn != position" @click="stand">
        STAND
      </button>
    </div>

    <div class="text-center h-25" v-if="gameState.status == GameStatus.ROUND_ENDED">
      <button v-if="gameState.players[position].status == PlayerStatus.LOBBY_WAITING" class="btn btn-outline-success fs-3 w-100 mt-3 custom-button" @click="ready">
        <div>
          [
          {{Object.values(gameState.players).filter(card => card.status === PlayerStatus.LOBBY_READY).length - 1}}
          /
          {{Object.values(gameState.players).filter(card => card.status === PlayerStatus.LOBBY_READY || card.status === PlayerStatus.LOBBY_WAITING).length - 1}}
          ]
        </div>
        <div class="fw-bold">{{ $t("message.ready") }}</div>
      </button>

      <button v-if="gameState.players[position].status == PlayerStatus.LOBBY_READY" class="btn btn-success fs-3 h-100 w-100 mt-3 custom-button" disabled>
        <div>
          [
          {{Object.values(gameState.players).filter(card => card.status === PlayerStatus.LOBBY_READY).length - 1}}
          /
          {{Object.values(gameState.players).filter(card => card.status === PlayerStatus.LOBBY_READY || card.status === PlayerStatus.LOBBY_WAITING).length - 1}}
          ]
        </div>
        <div>{{ $t("message.ready") }}</div>
      </button>
    </div>
    <button class="btn btn-danger w-100 my-4" v-if="gameState.status === GameStatus.ROUND_ENDED || gameState.status === GameStatus.NOT_STARTED" @click="disconnect">
      {{ $t("message.disconnect") }}
    </button>
  </div>
</template>