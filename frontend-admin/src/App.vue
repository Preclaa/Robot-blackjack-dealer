<script setup lang="ts">

import LogMessages from '@/components/LogMessages.vue'
import PlayerList from '@/components/PlayerList.vue'

import ArcorSettings from '@/components/ArcorSettings.vue'
import GameSettings from '@/components/GameSettings.vue'
import CameraSettings from '@/components/CameraSettings.vue'
import DebugOptions from '@/components/DebugOptions.vue'
import QrCode from '@/components/QrCode.vue'

import PoseSettings from '@/components/PoseSettings.vue'
import SavedPoses from '@/components/SavedPoses.vue'
import CustomPoses from '@/components/CustomPoses.vue'
import SceneVisualizer from '@/components/SceneVisualizer.vue'

</script>

<template>
  <div class="container-fluid">
    <div class="row vh-100">
      <div class="col-12 col-md-3 bg-light text-white p-5 d-flex flex-column vh-100 overflow-auto">

        <div class="accordion mt-3" id="gameAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingGame">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseGame" aria-expanded="false" aria-controls="collapseGame">
                GAME
              </button>
            </h2>
            <div id="collapseGame" class="accordion-collapse collapse show" aria-labelledby="headingGame" data-bs-parent="#gameAccordion">
              <div class="accordion-body">
                <GameSettings />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="arcor2Accordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingArcor2">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseArcor2" aria-expanded="true" aria-controls="collapseArcor2">
                ARCOR2 API
              </button>
            </h2>
            <div id="collapseArcor2" class="accordion-collapse collapse show" aria-labelledby="headingArcor2" data-bs-parent="#arcor2Accordion">
              <div class="accordion-body">
                <ArcorSettings />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="cameraAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingCamera">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCamera" aria-expanded="true" aria-controls="collapseCamera">
                Camera
              </button>
            </h2>
            <div id="collapseCamera" class="accordion-collapse collapse show" aria-labelledby="headingCamera" data-bs-parent="#cameraAccordion">
              <div class="accordion-body">
                <CameraSettings />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="debugAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingDebug">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCalibration" aria-expanded="true" aria-controls="collapseCalibration">
                Debug
              </button>
            </h2>
            <div id="collapseCalibration" class="accordion-collapse collapse show" aria-labelledby="headingDebug" data-bs-parent="#debugAccordion">
              <div class="accordion-body">
                <DebugOptions />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="qrCodesAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingQrCodes">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseQrCodes" aria-expanded="true" aria-controls="collapseQrCodes">
                QR Codes
              </button>
            </h2>
            <div id="collapseQrCodes" class="accordion-collapse collapse show" aria-labelledby="headingQrCodes" data-bs-parent="#qrCodesAccordion">
              <div class="accordion-body">
                <QrCode />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-5 p-5 d-flex flex-column">
        <PlayerList />
        <LogMessages />
      </div>

      <div class="col-12 col-md-4 bg-secondary text-white p-5 d-flex flex-column vh-100 overflow-auto">
        <div class="accordion mt-3" id="poseAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingPose">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePose" aria-expanded="true" aria-controls="collapsePose">
                Pose
              </button>
            </h2>
            <div id="collapsePose" class="accordion-collapse collapse show" aria-labelledby="headingPose" data-bs-parent="#poseAccordion">
              <div class="accordion-body">
                <PoseSettings />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="savedPositionsAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingSavedPositions">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSavedPositions" aria-expanded="true" aria-controls="collapseSavedPositions">
                Saved Positions
              </button>
            </h2>
            <div id="collapseSavedPositions" class="accordion-collapse collapse show" aria-labelledby="headingSavedPositions" data-bs-parent="#savedPositionsAccordion">
              <div class="accordion-body">
                <SavedPoses />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="customPositionsAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingCustomPositions">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCustomPositions" aria-expanded="true" aria-controls="collapseCustomPositions">
                Custom Positions
              </button>
            </h2>
            <div id="collapseCustomPositions" class="accordion-collapse collapse show" aria-labelledby="headingCustomPositions" data-bs-parent="#customPositionsAccordion">
              <div class="accordion-body">
                <CustomPoses />
              </div>
            </div>
          </div>
        </div>

        <div class="accordion mt-3" id="sceneAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingScene">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseScene" aria-expanded="true" aria-controls="collapseScene">
                Scene visualizer
              </button>
            </h2>
            <div id="collapseScene" class="accordion-collapse collapse show" aria-labelledby="headingScene" data-bs-parent="#sceneAccordion">
              <div class="accordion-body">
                <SceneVisualizer />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
