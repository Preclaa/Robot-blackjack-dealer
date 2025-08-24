<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

import { endpoint } from '@/utils/api'
import { poseStore } from '@/stores/pose'

const pose = poseStore()
const customPositions = ref<string[]>([])

const createPosition = () => {
    const positionName = prompt('Position name:')
    if (positionName) {
        axios
            .put(endpoint(`/pose_custom/set/${positionName}`))
            .then(() => {
                loadCustomPositions()
            })
            .catch((error) => {
                console.error('Error:', error)
            })
    }
}

const deletePosition = (name: string) => {
    axios
        .delete(endpoint(`/pose_custom/delete/${name}`))
        .then((response) => {
            loadCustomPositions()
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const loadCustomPositions = () => {
    axios
        .get(endpoint(`/pose_custom`))
        .then((response) => {
            customPositions.value = response.data
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const movePoseCustom = (key: string) => {
    axios
        .post(endpoint(`/pose_custom/move/${key}`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const setPoseCustom = (key: string) => {
    axios
        .put(endpoint(`/pose_custom/set/${key}`))
        .then((response) => {

        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

loadCustomPositions()
</script>

<template>
    <button class="btn btn-success w-100 mb-3" @click="() => createPosition()">
        Save New Position
    </button>
    <div class="d-flex justify-content-between mb-2" v-for="(position, index) in customPositions" :key="index">
        <span style="width: 25%">{{ position }}</span>
        <button class="btn btn-primary me-2" @click="() => setPoseCustom(position)">
            Set Pose
        </button>
        <button class="btn btn-secondary me-2" @click="() => movePoseCustom(position)">
            Move
        </button>
        <button class="btn btn-danger" @click="() => deletePosition(position)">
            <i class="bi bi-trash"></i>
        </button>
    </div>
</template>