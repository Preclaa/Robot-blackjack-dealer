<script setup lang="ts">
import QrcodeVue from 'qrcode.vue'

const QR_CODE_URL = import.meta.env.VITE_QR_CODE_URL
</script>

<template>
    <ul class="nav nav-tabs" id="playerTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link btn-sm active" id="player1-tab" data-bs-toggle="tab" data-bs-target="#player1" type="button" role="tab" aria-controls="player1" aria-selected="true">
                Player 1
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link btn-sm" id="player2-tab" data-bs-toggle="tab" data-bs-target="#player2" type="button" role="tab" aria-controls="player2" aria-selected="false">
                Player 2
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link btn-sm" id="player3-tab" data-bs-toggle="tab" data-bs-target="#player3" type="button" role="tab" aria-controls="player3" aria-selected="false">
                Player 3
            </button>
        </li>
    </ul>
    <div class="tab-content mt-3" id="playerTabsContent">
        <div class="tab-pane fade show active" id="player1" role="tabpanel" aria-labelledby="player1-tab">
            <qrcode-vue :value="`${QR_CODE_URL}?position=1`" render-as="svg" class="w-100 h-100" />
        </div>
        <div class="tab-pane fade" id="player2" role="tabpanel" aria-labelledby="player2-tab">
            <qrcode-vue :value="`${QR_CODE_URL}?position=2`" render-as="svg" class="w-100 h-100" />
        </div>
        <div class="tab-pane fade" id="player3" role="tabpanel" aria-labelledby="player3-tab">
            <qrcode-vue :value="`${QR_CODE_URL}?position=3`" render-as="svg" class="w-100 h-100" />
        </div>
    </div>
</template>