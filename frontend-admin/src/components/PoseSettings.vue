<script setup lang="ts">
import { ref } from 'vue'

import axios from 'axios'
import { endpoint } from '@/utils/api'
import type { Pose } from '@/types/types'
import { poseStore } from '@/stores/pose'
const pose = poseStore()

const moveOffset = ref(0.1)
const rotateAngle = ref(10)

import { Quaternion, Euler, MathUtils } from 'three';

const quaternionToEuler = (pose: Pose) => {
    const quaternion = new Quaternion(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w);
    const euler = new Euler().setFromQuaternion(quaternion, 'XYZ');

    return {
        x: MathUtils.radToDeg(euler.x),
        y: MathUtils.radToDeg(euler.y),
        z: MathUtils.radToDeg(euler.z),
    };
};

const move = (x: number, y: number, z: number) => {
    axios
        .post(endpoint(`/move/position?offset_x=${x}&offset_y=${y}&offset_z=${z}`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Move error:', error)
        })
}

const rotate = (axis: string, angle: number) => {
    axios
        .post(endpoint(`/move/rotation?axis=${axis}&angle=${angle}`))
        .then((response) => {
            pose.setPose(response.data)
        })
        .catch((error) => {
            console.error('Rotate error:', error)
        })
}


</script>

<template>
    <div class="accordion" id="positionAccordion">
        <div class="accordion-item">
            <h2 class="accordion-header" id="headingPosition">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePosition" aria-expanded="true" aria-controls="collapsePosition">
                    Position
                </button>
            </h2>
            <div id="collapsePosition" class="accordion-collapse collapse show" aria-labelledby="headingPosition" data-bs-parent="#positionAccordion">
                <div class="accordion-body">
                    <div class="row text-center">
                        <div class="col">
                            <div class="fw-bold">X</div>
                            <div>{{ pose.pose.position.x.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Y</div>
                            <div>{{ pose.pose.position.y.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Z</div>
                            <div>{{ pose.pose.position.z.toFixed(3) }}</div>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col">
                            <div class="d-flex flex-column justify-content-center align-items-center h-100">
                                <label for="moveOffset" class="form-label">Move offset</label>
                                <input type="text" class="form-control text-center border-secondary" id="moveOffset" v-model="moveOffset" />
                            </div>
                        </div>
                        <!-- style="transform: rotateX(50deg)" -->
                        <div class="col">
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 rounded-top w-100 " @click="() => move(moveOffset, 0, 0)">
                                    <i class="bi bi-arrow-up"></i>
                                </button>
                            </div>
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 w-100" @click="() => move(0, 0, moveOffset)">
                                    <i class="bi bi-arrow-left"></i>
                                </button>
                                <button class="btn btn-outline-secondary rounded-0 w-100" @click="() => move(0, 0, -moveOffset)">
                                    <i class="bi bi-arrow-right"></i>
                                </button>
                            </div>
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 rounded-bottom w-100" @click="() => move(-moveOffset, 0, 0)">
                                    <i class="bi bi-arrow-down"></i>
                                </button>
                            </div>
                        </div>
                        <div class="col">
                            <div class="d-flex flex-column justify-content-center align-items-center h-100">
                                <button class="btn btn-outline-secondary rounded-0 rounded-top w-100" @click="() => move(0, -moveOffset, 0)">
                                    <i class="bi bi-arrow-up"></i>
                                </button>
                                <button class="btn btn-outline-secondary rounded-0 rounded-bottom w-100" @click="() => move(0, moveOffset, 0)">
                                    <i class="bi bi-arrow-down"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="accordion mt-3" id="orientationAccordion">
        <div class="accordion-item">
            <h2 class="accordion-header" id="headingOrientation">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOrientation" aria-expanded="true" aria-controls="collapseOrientation">
                    Orientation
                </button>
            </h2>
            <div id="collapseOrientation" class="accordion-collapse collapse show" aria-labelledby="headingOrientation" data-bs-parent="#orientationAccordion">
                <div class="accordion-body">
                    <div class="row text-center">
                        <div class="col">
                            <div class="fw-bold">X</div>
                            <div>{{ pose.pose.orientation.x.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Y</div>
                            <div>{{ pose.pose.orientation.y.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Z</div>
                            <div>{{ pose.pose.orientation.z.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">W</div>
                            <div>{{ pose.pose.orientation.w.toFixed(3) }}</div>
                        </div>
                    </div>

                    <div class="row text-center bg-light py-2">
                        <div class="col">
                            <div class="fw-bold">X</div>
                            <div>{{ quaternionToEuler(pose.pose).x.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Y</div>
                            <div>{{ quaternionToEuler(pose.pose).y.toFixed(3) }}</div>
                        </div>
                        <div class="col">
                            <div class="fw-bold">Z</div>
                            <div>{{ quaternionToEuler(pose.pose).z.toFixed(3) }}</div>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col">
                            <div class="d-flex flex-column justify-content-center align-items-center h-100">
                                <label for="rotateAngle" class="form-label">Angle</label>
                                <input type="text" class="form-control text-center border-secondary" id="rotateAngle" v-model="rotateAngle" />
                            </div>
                        </div>

                        <div class="col">
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 rounded-top w-100" @click="() => rotate('y', -rotateAngle)">
                                    <i class="bi bi-arrow-up"></i>
                                </button>
                            </div>
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 w-100" @click="() => rotate('x', rotateAngle)">
                                    <i class="bi bi-arrow-left"></i>
                                </button>
                                <button class="btn btn-outline-secondary rounded-0 w-100" @click="() => rotate('x', -rotateAngle)">
                                    <i class="bi bi-arrow-right"></i>
                                </button>
                            </div>
                            <div class="d-flex justify-content-center align-items-center">
                                <button class="btn btn-outline-secondary rounded-0 rounded-bottom w-100" @click="() => rotate('y', rotateAngle)">
                                    <i class="bi bi-arrow-down"></i>
                                </button>
                            </div>
                        </div>
                        <div class="col">
                            <div class="d-flex flex-column justify-content-center align-items-center h-100">
                                <button class="btn btn-outline-secondary rounded-0 rounded-top w-100" @click="() => rotate('z', rotateAngle)">
                                    <i class="bi bi-arrow-clockwise"></i>
                                </button>
                                <button class="btn btn-outline-secondary rounded-0 rounded-bottom w-100" @click="() => rotate('z', -rotateAngle)">
                                    <i class="bi bi-arrow-counterclockwise"></i>
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>