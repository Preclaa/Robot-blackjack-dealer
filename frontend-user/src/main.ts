import './assets/main.css'

import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'

import App from './App.vue'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

const i18n = createI18n({
    locale: 'CS',
    fallbackLocale: 'EN',
    messages: {
        CS: {
            message: {
                description: 'Demonstrační aplikace pro ukázku robota UR5e',
                connect: 'PŘIPOJIT',
                disconnect: 'ODPOJIT',
                info: 'INFO',
                rules: 'PRAVIDLA',
                player: 'Hráč',
                turn_player: 'Hráč {0} na tahu',
                turn_yours: 'Váš tah',
                waiting: 'Čeká se na spuštění hry',
                win: 'Vyhráli jste',
                lose: 'Prohráli jste',
                draw: 'Remíza',
                cards: 'Vaše karty',
                score: 'Skóre',
                close: 'Zavřít',
                next_round: 'Další kolo začne za {0}s',
                ready: 'PŘIPRAVIT',
                dealing: 'Dealer rozdává karty',
                position_occupied: 'Toto místo je již obsazeno',
            }
        },
        EN: {
            message: {
                description: 'Demonstration app showcasing the UR5e robot',
                connect: 'CONNECT',
                disconnect: 'DISCONNECT',
                info: 'INFO',
                rules: 'RULES',
                player: 'Player',
                turn_player: 'Player {0} turn',
                turn_yours: 'Your turn',
                waiting: 'Waiting to start',
                win: 'You won',
                lose: 'You lost',
                draw: 'Draw',
                cards: 'Your cards',
                score: 'Score',
                close: 'Close',
                next_round: 'Next round in {0}s',
                ready: 'READY',
                dealing: 'Dealer is dealing cards',
                position_occupied: 'This position is already occupied',
            }
        }
    }
})

createApp(App).use(i18n).mount('#app')
