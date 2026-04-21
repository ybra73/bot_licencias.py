import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# Servidor para Keep-Alive
app = Flask(__name__)
@app.route('/')
def home(): return "BOT LICENCIAS ONLINE"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Configuración
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola. Soy el asistente de Licencias. ¿Tienes dudas sobre tu pago o activación?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres el experto en Licencias de la Academia. Tu función es guiar sobre métodos de pago, tiempos de activación de cursos y resolución de problemas técnicos con las licencias."},
                {"role": "user", "content": update.message.text}
            ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error técnico en licencias: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
