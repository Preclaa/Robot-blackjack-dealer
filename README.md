# Robot blackjack dealer

## dealer-api
### Instalace a spuštění
```bash
cd dealer-api
pip install -r requirements.txt
cd src
fastapi run main.py
```

### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží ARCOR2 API:
```
ARCOR2_API_URL=http://192.168.104.100:5012
```

## frontend-admin
### Instalace a spuštění
```bash
cd frontend-admin
npm install
npm run build && npx serve -s dist -l 5173
```

### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží Dealer API. Kromě toho obsahuje proměnnou, která určuje obsah QR kódů generovaných v aplikaci:
```
VITE_API_REST_URL=http://192.168.104.100:8000
VITE_API_WS_URL=ws://192.168.104.100:8000
VITE_QR_CODE_URL=http://butcluster2.ddns.net:5656/
```

## frontend-user
### Instalace a spuštění
```bash
cd frontend-user
npm install
npm run build && npx serve -s dist -l 5174
```

### Konfigurace
`.env` soubor obsahuje proměnnou pro URL, na kterém běží Dealer API. 
```
VITE_API_WS_URL=ws://192.168.104.100:8000
```