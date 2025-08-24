<script setup lang="ts">
import axios from 'axios'
import { endpoint } from '@/utils/api'


const screenshot = () => {
    axios
        .post(endpoint(`/debug/screenshot`))
        .then((response) => {
            console.log('Screenshot success:', response)
        })
        .catch((error) => {
            console.error('Screenshot error:', error)
        })
}

const turnCard = () => {
    axios
        .post(endpoint(`/debug/flip`))
        .then((response) => {
            console.log('Flip success:', response)
        })
        .catch((error) => {
            console.error('Flip error:', error)
        })
}

const detectCard = () => {
    axios
        .post(endpoint(`/debug/detect`))
        .then((response) => {
            console.log('Detect success:', response)
        })
        .catch((error) => {
            console.error('Detect error:', error)
        })
}

const dealCards = () => {
    axios
        .post(endpoint(`/debug/deal`))
        .then((response) => {
            console.log('Deal success:', response)
        })
        .catch((error) => {
            console.error('Deal error:', error)
        })
}

</script>

<template>
    <button class="btn btn-primary w-100 mt-2" @click="() => dealCards()">
        DEAL CARDS
    </button>

    <button class="btn btn-primary w-100 mt-2" @click="() => turnCard()">
        TURN CARD
    </button>

    <button class="btn btn-primary w-100 mt-2" @click="() => detectCard()">
        DETECT CARD
    </button>
    <button class="btn btn-primary w-100 mt-2" @click="() => screenshot()">
        TAKE SCREENSHOT
    </button>
</template>