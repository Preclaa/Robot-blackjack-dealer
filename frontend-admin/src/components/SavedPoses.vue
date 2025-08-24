<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Position } from '@/types/types'

import { poseStore } from '@/stores/pose'
const pose = poseStore()

import axios from 'axios'
import { endpoint } from '@/utils/api'

const activeConfiguration = ref<string>("default")
const configurations = ref<string[]>([])
const offsets = ref<Record<string, Position>>({})

const editMode = ref(false)

const changeConfiguration = () => {
    axios
        .put(endpoint(`/configuration/active/${activeConfiguration.value}`))
        .then(() => {
            loadConfigurations()
            loadOffsets()
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const createConfiguration = () => {
    const configurationName = prompt('Position name:')
    if (configurationName) {
        axios
            .put(endpoint(`/configuration/new/${configurationName}`))
            .then(() => {
                activeConfiguration.value = configurationName
                loadConfigurations()
                loadOffsets()
            })
            .catch((error) => {
                console.error('Error:', error)
            })
    }
}

const deleteConfiguration = () => {
    axios
        .delete(endpoint(`/configuration/delete/${activeConfiguration.value}`))
        .then(() => {
            activeConfiguration.value = "default"
            loadConfigurations()
            loadOffsets()
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const setDeckPose = () => {
    axios
        .put(endpoint(`/configuration/deck/set`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const moveDeckPose = () => {
    axios
        .post(endpoint(`/configuration/deck/move`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const moveOffsetPose = (key: string) => {
    axios
        .post(endpoint(`/configuration/offset/${key}`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const loadConfigurations = async () => {
    axios
        .get(endpoint(`/configuration/keys`))
        .then((response) => {
            const result = response.data
            configurations.value = result
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const loadOffsets = async () => {
    axios
        .get(endpoint(`/configuration/offsets`))
        .then((response) => {
            offsets.value = response.data
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

const saveEdit = async () => {
    axios
        .put(endpoint(`/configuration/offsets`), offsets.value)
        .then(() => {
            loadOffsets()
        })
        .catch((error) => {
            console.error('Error:', error)
        })
    editMode.value = false

}

const cancelEdit = () => {
    loadOffsets()
    editMode.value = false
}

onMounted(() => {
    loadOffsets()
    loadConfigurations()
})

</script>

<template>
    <div class="d-flex justify-content-between mb-3">
        <select class="form-select w-50 me-2" v-model="activeConfiguration" @change="changeConfiguration" :disabled="editMode">
            <option v-for="configuration in configurations" :key="configuration" :value="configuration">
                {{ configuration }}
            </option>
        </select>

        <div>
            <button v-if="!editMode" class="btn btn-success ms-2" title="Add" @click="createConfiguration">
                <i class="bi bi-plus"></i>
            </button>
            <button v-if="!editMode" class="btn btn-danger ms-2" title="Delete" @click="deleteConfiguration">
                <i class="bi bi-trash"></i>
            </button>
        </div>
    </div>

    <div class="d-flex justify-content-between my-3">
        <span style="width: 25%">Deck</span>
        <button class="btn btn-primary me-2 w-50" @click="() => setDeckPose()">
            Set Pose
        </button>
        <button class="btn btn-secondary" @click="() => moveDeckPose()">
            <i class="bi bi-box-arrow-in-right"></i>
        </button>
    </div>

    <div>
        <div v-for="(offset, key) in offsets" :key="key" class="d-flex justify-content-between mb-2">
            <div class="col">{{ key }}</div>
            <input v-model.number="offsets[key].x" class="col form-control form-control-sm mx-1 text-center" :disabled="!editMode" style="max-width: 70px;" />
            <input v-model.number="offsets[key].y" class="col form-control form-control-sm mx-1 text-center" :disabled="!editMode" style="max-width: 70px;" />
            <input v-model.number="offsets[key].z" class="col form-control form-control-sm mx-1 text-center" :disabled="!editMode" style="max-width: 70px;" />
            <button class="btn btn-secondary ms-2" @click="() => moveOffsetPose(key)">
                <i class="bi bi-box-arrow-in-right"></i>
            </button>
        </div>
    </div>

    <div class="d-flex justify-content-end mt-3">
        <button v-if="!editMode" class="btn btn-outline-secondary w-100" title="Edit" @click="editMode = true">
            <i class="bi bi-pencil"></i>
        </button>
        <button v-if="editMode" class="btn btn-success w-50" title="Save" @click="saveEdit">
            <i class="bi bi-check"></i>
        </button>
        <button v-if="editMode" class="btn btn-danger ms-2 w-50" title="Cancel" @click="cancelEdit">
            <i class="bi bi-x"></i>
        </button>
    </div>

</template>