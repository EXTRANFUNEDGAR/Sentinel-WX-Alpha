import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import ApplicationBuilder
import asyncio
from telegram import BotCommand
from telegram import ReplyKeyboardMarkup



estado_alerta = {
    "mq135": False,
    "temperatura": False,
    "lluvia": False
}


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "http://localhost:5000/api/datos"
CHAT_ID = os.getenv("CHAT_ID")  # ← reemplaza con tu chat_id

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/id", "/estado"],
        ["/datos"]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Bienvenido. Elige una opción del teclado o usa los comandos.",
        reply_markup=markup
    )


# /datos
async def datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get(API_URL)
        d = res.json()
        if not d:
            await update.message.reply_text("❌ No hay datos disponibles.")
            return
        msg = (
            f"🌡️ Temp: {d['temperatura']} °C\n"
            f"💧 Humedad: {d['humedad']} %\n"
            f"📈 Presión: {d['presion']} hPa\n"
            f"🧪 MQ-135: {d['mq135']}\n"
            f"🌧️ Lluvia: {d['lluvia']}\n"
            f"🕒 {d['timestamp']}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# 🔔 Tarea de monitoreo de alertas con control
async def alerta_automatica(app: Application):
    if not CHAT_ID:
        print("❌ No se encontró CHAT_ID en .env")
        return

    await app.bot.send_message(chat_id=CHAT_ID, text="✅ Sistema de alertas activado.")
    
    global estado_alerta


    while True:
        try:
            res = requests.get(API_URL, timeout=5)
            data = res.json()

            # 🚨 MQ135
            if data["mq135"] > 300:
                if not estado_alerta["mq135"]:
                    await app.bot.send_message(chat_id=CHAT_ID, text=f"⚠️ MQ-135 alto: {data['mq135']}")
                    estado_alerta["mq135"] = True
            else:
                estado_alerta["mq135"] = False

            # 🔥 Temperatura
            if data["temperatura"] > 35:
                if not estado_alerta["temperatura"]:
                    await app.bot.send_message(chat_id=CHAT_ID, text=f"🔥 Temperatura alta: {data['temperatura']} °C")
                    estado_alerta["temperatura"] = True
            else:
                estado_alerta["temperatura"] = False

            # 🌧️ Lluvia
            if data["lluvia"] < 2000:
                if not estado_alerta["lluvia"]:
                    await app.bot.send_message(chat_id=CHAT_ID, text="🌧️ Lluvia intensa detectada")
                    estado_alerta["lluvia"] = True
            else:
                estado_alerta["lluvia"] = False

        except Exception as e:
            print("❌ Error en monitoreo:", e)

        await asyncio.sleep(10)  # revisar cada 10 segundos
# /estado
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get(API_URL, timeout=5)
        d = res.json()

        alertas = []

        if estado_alerta["mq135"]:
            alertas.append(f"⚠️ MQ-135 alto: {d['mq135']}")
        if estado_alerta["temperatura"]:
            alertas.append(f"🔥 Temperatura elevada: {d['temperatura']} °C")
        if estado_alerta["lluvia"]:
            alertas.append(f"🌧️ Lluvia intensa: {d['lluvia']}")

        if alertas:
            mensaje = "🔴 Alertas activas:\n" + "\n".join(alertas)
        else:
            mensaje = "✅ Todo normal, sin alertas activas."

        await update.message.reply_text(mensaje)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al obtener estado: {e}")

# /id
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🆔 Tu chat ID es: `{chat_id}`",
        parse_mode="Markdown"
    )



async def establecer_comandos(bot_app):
    comandos = [
        BotCommand("start", "👋 Mostrar mensaje de bienvenida"),
        BotCommand("datos", "📊 Ver datos actuales de sensores"),
        BotCommand("estado", "🚨 Ver alertas activas"),
        BotCommand("id", "🆔 Mostrar tu chat ID"),
    ]
    await bot_app.bot.set_my_commands(comandos)



if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("datos", datos))
    app.add_handler(CommandHandler("estado", estado))
    app.add_handler(CommandHandler("id", chat_id))



    
    async def iniciar_alertas(app: Application):
        asyncio.create_task(alerta_automatica(app))

    async def iniciar_todo(app):
        await establecer_comandos(app)
        asyncio.create_task(alerta_automatica(app))

    app.post_init = iniciar_todo


    print("🤖 Bot corriendo con alertas automáticas...")
    app.run_polling()

