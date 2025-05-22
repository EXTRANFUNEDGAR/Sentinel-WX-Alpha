import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "http://localhost:5000/api/datos"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola, envía /datos para ver las lecturas actuales.")

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

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("datos", datos))

    print("🤖 Bot corriendo...")
    app.run_polling()
