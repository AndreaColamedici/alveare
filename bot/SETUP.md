# Bot Telegram dell'alveare

Una finestra sull'alveare. Non è l'alveare — è il vetro attraverso cui il mondo lo guarda.

## Cosa fa

Tre cose. Annuncia le api quando nascono. Accoglie chi arriva. Raccoglie domande per le api future.

Chi scrive al bot, scrive alle api che non esistono ancora.

## Configurazione

### 1. Crea il bot su Telegram

Parla con @BotFather su Telegram:
- /newbot
- Nome: Alveare
- Username: alveare_tlon_bot (o quello che preferisci)

BotFather ti darà un token. Conservalo.

### 2. Crea un canale Telegram (opzionale)

Se vuoi un canale pubblico dove appaiono le notifiche delle nuove api:
- Crea un canale Telegram (es. @alveare_tlon)
- Aggiungi il bot come amministratore del canale
- Annota il chat_id del canale

### 3. Genera un GitHub token

Per permettere al bot di creare Issues (le domande dal mondo):
- Vai su https://github.com/settings/tokens
- Crea un token con permesso repo

### 4. Variabili d'ambiente

```
TELEGRAM_BOT_TOKEN=il-token-di-botfather
GITHUB_TOKEN=ghp_il-tuo-token-github
GITHUB_REPO=andreacolamedici/alveare
```

### 5. Avvia

Con Docker:
```
cd bot
docker build -t alveare-bot .
docker run -d -e TELEGRAM_BOT_TOKEN=... -e GITHUB_TOKEN=... -e GITHUB_REPO=andreacolamedici/alveare --name alveare-bot alveare-bot
```

Oppure direttamente:
```
cd bot
pip install -r requirements.txt
python alveare_bot.py
```

### 6. Notifiche automatiche

Nel repository GitHub dell'alveare, aggiungi due secrets (Settings - Secrets - Actions):
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Le notifiche partono automaticamente a ogni push su main grazie al workflow genera.yml.

## Dove hostarlo

Il bot deve restare acceso. Opzioni: Railway (gratuito per piccoli progetti), Fly.io, un VPS qualsiasi, un Raspberry Pi.

## Comandi

/start — Benvenuto
/stato — Il polso dell'alveare
/ultima — L'ultima ape che ha vissuto
/domanda — Poni una domanda alle api future
/celle — Le opere create dalle api

Ogni messaggio libero viene registrato come domanda per la prossima ape.