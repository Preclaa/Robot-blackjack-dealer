<script setup lang="ts">
import { onMounted } from 'vue'
import { websocket } from '@/utils/api'

onMounted(() => {
    const videoElement = document.getElementById('camera') as HTMLVideoElement
    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        navigator.mediaDevices
            .enumerateDevices()
            .then(async (devices) => {
                const externalCameras = devices.filter(
                    (device) => device.kind === 'videoinput' && !device.label.toLowerCase().includes('integrated'),
                )
                if (externalCameras.length > 0) {
                    const externalCameraId = externalCameras[0].deviceId
                    return navigator.mediaDevices.getUserMedia({
                        video: {
                            deviceId: externalCameraId,
                            width: { ideal: 1920 },
                            height: { ideal: 1080 }
                        },
                    })
                } else {
                    throw new Error('No camera found')
                }
            })
            .then((stream) => {
                videoElement.srcObject = stream
            })
            .catch((error) => {
                console.error(error)
            })
    }

    const ws_camera = websocket('/ws_camera')
    ws_camera.onopen = () => {
        console.log('Camera connected')
    }
    ws_camera.onmessage = (event) => {
        if (event.data == '') {
            // Request from server, send current frame from video
            const canvas = document.createElement('canvas')
            console.log(videoElement.videoWidth, videoElement.videoHeight)
            canvas.width = videoElement.videoWidth
            canvas.height = videoElement.videoHeight
            const context = canvas.getContext('2d')
            if (context) {
                context.drawImage(videoElement, 0, 0, canvas.width, canvas.height)
                const imageData = canvas.toDataURL('image/jpeg')
                ws_camera.send(imageData)
            }
        }
    }
    ws_camera.onerror = (error) => {
        console.error('WebSocket (camera) error:', error)
    }
    ws_camera.onclose = () => {
        console.log('WebSocket (camera) connection closed')
    }
})
</script>

<template>
    <video id="camera" autoplay playsinline class="w-100"></video>
</template>