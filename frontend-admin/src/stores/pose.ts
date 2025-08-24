import { defineStore } from 'pinia'
import type { Pose } from '@/types/types'

export const poseStore = defineStore('pose', {
    state: (): { pose: Pose } => ({
        pose: {
            orientation: {
                w: 0,
                x: 0,
                y: 0,
                z: 0,
            },
            position: {
                x: 0,
                y: 0,
                z: 0,
            },
        },
    }),
    actions: {
        setPose(newPose: Pose) {
            this.pose = newPose
        },
    },
})