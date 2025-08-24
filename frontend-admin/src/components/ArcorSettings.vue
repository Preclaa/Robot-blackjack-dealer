<script setup lang="ts">

import { ref } from 'vue'

import axios from 'axios'
import { endpoint } from '@/utils/api'

const robotVelocity = ref(50)

const startApi = () => {
    axios
        .post(endpoint(`/arcor/start`))
        .then((response) => {
            console.log('ARCOR2 Start success:', response)
        })
        .catch((error) => {
            console.error('ARCOR2 Start error:', error)
        })
}

const stopApi = () => {
    axios
        .post(endpoint(`/arcor/stop`))
        .then((response) => {
            console.log('ARCOR2 success:', response)
        })
        .catch((error) => {
            console.error('ARCOR2 error:', error)
        })
}

const suction = (state: boolean) => {
    axios
        .put(endpoint(`/suction/${state}`))
        .then((response) => {
            console.log('Suction success:', response)
        })
        .catch((error) => {
            console.error('Suction error:', error)
        })
}

const setVelocity = (velocity: number) => {
    axios
        .put(endpoint(`/velocity/${velocity}`))
        .then((response) => {
            console.log('Velocity uccess:', response)
        })
        .catch((error) => {
            console.error('Velocity error:', error)
        })
}
</script>

<template>
    <button class="btn btn-primary w-100" @click="startApi">START API</button>
    <button class="btn btn-danger w-100 mt-2" @click="stopApi">STOP API</button>
    <button class="btn btn-secondary w-100 mt-2" @click="() => suction(true)">
        SUCTION ON
    </button>
    <button class="btn btn-secondary w-100 mt-2" @click="() => suction(false)">
        SUCTION OFF
    </button>
    <div class="mt-3">
        <label for="slider" class="form-label">Robot velocity: {{ robotVelocity }}</label>
        <input type="range" step="5" class="form-range" id="slider" min="0" max="100" v-model="robotVelocity" @change="() => setVelocity(robotVelocity)" />
    </div>
</template>