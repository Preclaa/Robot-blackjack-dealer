# Robot blackjack dealer
Diplomová práce

Systém pro ovládání robotického ramene UR5e, který demonstruje schopnosti robota prostřednictvím interaktivní ukázky karetní hry blackjack. Systém umožňuje hráčům zapojit se do hry pomocí mobilního zařízení, zatímco robotické rameno slouží jako dealer, který rozdává a manipuluje s hracími kartami. 

<img width="800" alt="image" src="https://github.com/user-attachments/assets/badff3ce-0094-4243-938b-75c0d7e13855" />

<img width="800" alt="image" src="https://github.com/user-attachments/assets/4e21e7cb-9f6b-43fe-9387-6dcd28e94b2b" />

## Ukázka

https://github.com/user-attachments/assets/71b9e205-7dcb-469f-9c0f-5c6d4f50145d


## Instalace
### arcor2
[https://github.com/robofit/arcor2](https://github.com/robofit/arcor2)
### dealer-api
#### Instalace a spuštění
```bash
cd dealer-api
pip install -r requirements.txt
cd src
fastapi run main.py
```

#### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží ARCOR2 API:
```
ARCOR2_API_URL=http://192.168.104.100:5012
```

### frontend-admin
#### Instalace a spuštění
```bash
cd frontend-admin
npm install
npm run build && npx serve -s dist -l 5173
```

#### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží Dealer API. Kromě toho obsahuje proměnnou, která určuje obsah QR kódů generovaných v aplikaci:
```
VITE_API_REST_URL=http://192.168.104.100:8000
VITE_API_WS_URL=ws://192.168.104.100:8000
VITE_QR_CODE_URL=http://butcluster2.ddns.net:5656/
```

### frontend-user
#### Instalace a spuštění
```bash
cd frontend-user
npm install
npm run build && npx serve -s dist -l 5174
```



#### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží Dealer API. 
```
VITE_API_WS_URL=ws://192.168.104.100:8000
```
