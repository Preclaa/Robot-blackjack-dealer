<script setup lang="ts">

import { ref } from 'vue'
import { websocket } from '@/utils/api'

import type { LogMessage } from '@/types/types'

const log = ref<LogMessage[]>([])

const ws_log = websocket('/ws_log')
ws_log.onopen = () => {
    console.log('WebSocket (log) connection established')
}
ws_log.onmessage = (event) => {
    const result = JSON.parse(event.data)
    log.value.unshift(result)
}
ws_log.onerror = (error) => {
    console.error('WebSocket (log) error:', error)
}
ws_log.onclose = () => {
    console.log('WebSocket (log) connection closed')
}

const logBackground = (level: string) => {
    switch (level) {
        case 'INFO':
            return 'bg-info'
        case 'ERROR':
            return 'bg-danger'
        case 'WARNING':
            return 'bg-warning'
        case 'DEBUG':
            return 'bg-secondary'
        default:
            return ''
    }
}
</script>

<template>
    <h3 class="mt-auto">Log</h3>
    <div class="chat-log border rounded p-2 bg-white" style="height: 300px; overflow-y: auto">
        <div v-for="(message, index) in log" :key="index" class="small">
            <div>
                {{ new Date(message.time).toLocaleTimeString('en-US', { hour12: false }) }}
                <span class="log-type small text-white p-1" :class="logBackground(message.type)">{{ message.type }}</span>
                {{ message.message }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.log-type {
    width: 50px;
    display: inline-block;
    text-align: center;
    padding: 0 !important;
    padding-bottom: 2px !important;
}
</style>
