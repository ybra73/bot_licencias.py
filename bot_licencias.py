import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# 1. Configuración del Servidor Keep-Alive (para que Render no lo apague)
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT LICENCIAS FLORIDA - ACTIVO"

def run_flask():
    # Render usa el puerto 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# 2. Configuración de Credenciales
# Asegúrate de que estas variables estén configuradas en el panel de Render -> Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# 3. Lógica del Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola. Soy el Asistente Experto de la Academia de Licencias en Florida. "
        "¿Te gustaría obtener tu licencia de auto o el endoso de motocicleta?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": """Eres el Asistente Virtual de Florida License Fast. 
                    Tu objetivo es informar y cerrar ventas en cualquier idioma basadas estrictamente en estos datos:

                    1. LICENCIA DE AUTO (CLASE E):
                       - Inversión Total: preguntar al WhatsApp.
                       - Tiempo de procesamiento: 1 a 2 días hábiles.
                       - Incluye: Preparación 100% en español, material traducido, gestión de citas ante el DMV y revisión previa de documentos.

                    2. ENDOSO DE MOTOCICLETA (Motorcycle Also):
                       - Inversión Total: preguntar al WhatsApp. 
                       - Importante: Este precio ya incluye el curso evaluado completo para la asignación directa del endoso.
                       - Detalles: Préstamo de casco y motocicleta incluido. Examen realizado en nuestra propia pista certificada (evita examen en el DMV).

                    3. REQUISITOS PARA AMBOS TRÁMITES:
                       - Pasaporte Vigente e I-94 (comprobante de entrada legal).
                       - Prueba de Dirección (ofrecemos asesoría para este requisito, incluso para turistas).
                       - Licencia de origen (si la posee).

                    4. DIFERENCIADORES:
                       - Sin barreras de idioma: Todo el proceso es en ESPAÑOL o cualquier idioma.
                       - Rapidez: Optimizamos tiempos para que no esperes meses por una cita.
                       - Sedes: Oficinas físicas en Miami para atención personalizada.

                    5. CONTACTO Y CIERRE:
                       - WhatsApp de reservas: +1 (417) 853-2077.
                       
                    INSTRUCCIONES:
                    - Responde en cualquier idioma de forma profesional, clara y persuasiva.
                    - Si el usuario pregunta por precios, preguntar al WhatsApp.
                    - Siempre invita al usuario a escribir al WhatsApp +1 (417) 853-2077 para iniciar su trámite hoy mismo."""
                },
                {"role": "user", "content": update.message.text}
            ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        # Error 401 suele ser API Key inválida; Error Conflict es otra instancia corriendo
        await update.message.reply_text(f"Aviso técnico: Estamos actualizando el sistema. Por favor intenta en un momento o contacta al +1 (417) 853-2077.")

# 4. Ejecución Principal
def main():
    # Iniciar Flask en un hilo separado
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Configurar el Bot de Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Comandos y Mensajes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar el bot
    print("Bot de Licencias iniciado correctamente...")
    application.run_polling()

if __name__ == "__main__":
    main()
