<script setup lang="ts">
import { TresCanvas } from '@tresjs/core'
import { OrbitControls } from '@tresjs/cientos'


import type { Position } from '@/types/types'

import axios from 'axios'
import { endpoint } from '@/utils/api'

import { ref } from 'vue'

const scene_positions = ref<Record<string, Position[]>>({})

const loadScene = () => {
    axios
        .get(endpoint('/scene'))
        .then((response) => {
            scene_positions.value = response.data
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

loadScene()

</script>

<template>
    <div class="row mb-3">
        <div class="col-3 d-flex align-items-center gap-2">
            <span class="color-box" style="background: red"></span>
            <span>Deck</span>
        </div>
        <div class="col-3 d-flex align-items-center gap-2">
            <span class="color-box" style="background: blue"></span>
            <span>Dealer</span>
        </div>
        <div class="col-3 d-flex align-items-center gap-2">
            <span class="color-box" style="background: green"></span>
            <span>Player</span>
        </div>
        <div class="col-3 d-flex align-items-center gap-2">
            <span class="color-box" style="background: yellow"></span>
            <span>Custom</span>
        </div>
    </div>
    <div style="height: 250px;" v-if="Object.keys(scene_positions).length > 0">
        <TresCanvas>
            <TresPerspectiveCamera />
            <OrbitControls :target="[-scene_positions['deck'][0].x, -scene_positions['deck'][0].y, scene_positions['deck'][0].z]" />

            <TresMesh :position="[-scene_positions['deck'][0].x, -scene_positions['deck'][0].y, scene_positions['deck'][0].z]">
                <TresBoxGeometry :args="[0.05, 0.01, 0.08]" />
                <TresMeshBasicMaterial color="red" />
            </TresMesh>

            <TresMesh :position="[-scene_positions['dealer'][0].x, -scene_positions['dealer'][0].y, scene_positions['dealer'][0].z]">
                <TresBoxGeometry :args="[0.05, 0.01, 0.08]" />
                <TresMeshBasicMaterial color="blue" />
            </TresMesh>

            <TresMesh v-for="(playerPos, idx) in scene_positions['players']" :key="'player-' + idx" :position="[-playerPos.x, -playerPos.y, playerPos.z]">
                <TresBoxGeometry :args="[0.05, 0.01, 0.08]" />
                <TresMeshBasicMaterial color="green" />
            </TresMesh>

            <TresMesh v-for="(customPos, idx) in scene_positions['custom']" :key="'custom-' + idx" :position="[-customPos.x, -customPos.y, customPos.z]">
                <TresBoxGeometry :args="[0.05, 0.01, 0.08]" />
                <TresMeshBasicMaterial color="yellow" />
            </TresMesh>
        </TresCanvas>
    </div>
    <div class="w-100 text-center">
        <button class="btn btn-sm btn-secondary w-50" @click="loadScene">
            <i class="bi bi-arrow-clockwise"></i>
            Reload Scene
        </button>
    </div>
</template>

<style scoped>
.color-box {
    width: 20px;
    height: 20px;
    border: 1px solid black;
}
</style>