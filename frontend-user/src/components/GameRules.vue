<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
</script>

<template>
    <div v-if="locale === 'CS'">
        <p>
            Tato aplikace implementuje zjednodušenou verzi karetní hry <strong>Blackjack</strong>, ve které robot slouží jako dealer. Hra byla upravena tak, aby byla vhodná pro interaktivní demonstraci a ovládání přes mobilní zařízení.
        </p>
        <h4>Základní principy hry</h4>
        <p>
            Cílem hry je získat součet karet co nejblíže hodnotě 21, aniž byste ji překročili.
            Karty 2–10 mají svou číselnou hodnotu, obrázkové karty (J, Q, K) mají hodnotu 10.
            Eso má hodnotu 1 nebo 11, podle toho, co je výhodnější.
            Překročení 21 znamená automatickou prohru.
        </p>
        <h4>Průběh kola</h4>
        <ul>
            <li>Každý hráč dostane na začátku dvě karty.</li>
            <li>Hráči hrají jako první, jeden po druhém.</li>
            <li>Ve svém tahu máte dvě možnosti: <strong>HIT</strong> (vzít kartu), <strong>STAND</strong> (ukončit kolo).</li>
            <li>Po všech hráčích hraje dealer.</li>
        </ul>
        <h4>Rozdíly oproti klasickému blackjacku</h4>
        <ul>
            <li>Dealer dostává na začátku pouze jednu kartu.</li>
            <li>Není podporován <em>split</em>, <em>double down</em> ani jiné akce – pouze HIT a STAND.</li>
        </ul>
    </div>

    <div v-else>
        <p>
            This application implements a simplified version of the <strong>Blackjack</strong> card game, where the dealer is replaced by a robot. The game has been adapted for interactive demonstration and control via mobile devices.
        </p>
        <h4>Basic Game Principles</h4>
        <p>
            The goal is to reach a total card value as close as possible to 21 without going over.
            Cards 2–10 are worth their face value, face cards (J, Q, K) are worth 10,
            and an Ace counts as either 1 or 11 — whichever is more beneficial.
            Exceeding 21 results in an automatic loss.
        </p>
        <h4>Turn Sequence</h4>
        <ul>
            <li>Each player is dealt two cards at the beginning.</li>
            <li>Players take turns first, one by one.</li>
            <li>During your turn, you have two options: <strong>HIT</strong> (take a card), <strong>STAND</strong> (end your turn).</li>
            <li>After all players finish their turns, the dealer plays.</li>
        </ul>
        <h4>Differences from Traditional Blackjack</h4>
        <ul>
            <li>The dealer only receives one card at the beginning.</li>
            <li><em>Split</em>, <em>double down</em>, and other advanced actions are not supported – only HIT and STAND are available.</li>
        </ul>
    </div>
</template>