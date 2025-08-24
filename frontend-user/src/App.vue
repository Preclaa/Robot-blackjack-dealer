<script setup lang="ts">
import PlayerControls from '@/components/PlayerControls.vue'
import GameRules from '@/components/GameRules.vue'

import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const nextLanguage = computed(() => (locale.value === 'CS' ? 'EN' : 'CS'))
function toggleLanguage() {
  locale.value = nextLanguage.value
}

</script>

<template>
  <main>
    <div class="p-2 d-flex flex-column" style="height: 100dvh;">
      <div class="text-center">
        <h1 class="display-5 m-0 fw-bold">BLACKJACK</h1>
        <p class="text-secondary m-0">{{ $t("message.description") }}</p>
      </div>
      <hr />

      <PlayerControls />

      <hr />
      <div class="d-flex justify-content-center">
        <button class="btn btn-sm btn-outline-secondary mx-2 w-25" data-bs-toggle="modal" data-bs-target="#rulesModal">{{ $t("message.rules") }}</button>
        <button class="btn btn-sm btn-outline-secondary mx-2 w-25" @click="toggleLanguage">{{ nextLanguage }}</button>
      </div>
    </div>

    <div class="modal fade" id="rulesModal" tabindex="-1" aria-labelledby="rulesModalLabel" aria-hidden="true">
      <div class="modal-dialog d-flex h-100">
        <div class="modal-content my-auto">
          <div class="modal-header">
            <h5 class="modal-title" id="rulesModalLabel">{{ $t("message.rules") }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <GameRules />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ $t("message.close") }}</button>
          </div>
        </div>
      </div>
    </div>

  </main>
</template>