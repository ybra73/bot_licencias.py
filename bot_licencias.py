import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# 1. Configuración del Servidor Keep-Alive
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT LICENCIAS FLORIDA - ACTIVO"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# 2. Configuración de Credenciales
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# 3. Lógica del Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola. Soy el Asistente Experto de Florida License Fast. 🚗💨\n\n"
        "Te ayudo a obtener tu licencia de auto (Clase E) o el endoso de motocicleta de forma rápida. "
        "¿En qué puedo asesorarte hoy?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": """Eres el Asistente Virtual de Florida License Fast. 
                    Tu objetivo es informar y cerrar ventas basadas estrictamente en este entrenamiento:

                    1. DOCUMENTACIÓN OBLIGATORIA (Original, Vigente, Físico):
                    - Identificación Primaria: Pasaporte, Green Card, Permiso de Trabajo o SSN (si aplica).
                    - Identificación Secundaria: Licencia de origen, Acta de nacimiento/matrimonio o ID Nacional (Cédula).
                    - Estatus Migratorio: I-94 (Turista, visas F, J, O, U, E), Asilo, Ajuste Cubano o CBP ONE.
                    - Residencia en Florida: 2 documentos físicos de los últimos 30 días (bancos, servicios, renta). No se acepta Amazon/e-commerce.

                    2. PROCESO DE OBTENCIÓN:
                    - Paso 1 (TLSAE): Curso de alcohol y drogas. Se exime si tiene licencia física plástica de su país.
                    - Paso 2 (Teórico): 50 preguntas (aprueba con 40/80%). Otorga Permiso de Aprendizaje.
                    - Paso 3 (Práctico): Examen de conducción en nuestra pista certificada o ente oficial.
                    - Paso 4 (Vista): Obligatorio en oficinas del DMV.

                    3. PLANES DE SERVICIO:
                    - Plan Premium Integral: Licencia en max 2 días. Incluye capacitación, exámenes (teórico/práctico), curso TLSAE y acompañamiento.
                    - Gestión Examen Teórico: Capacitación + examen en sede + guía de trámite.
                    - Gestión Examen Práctico: Para quienes ya tienen permiso. Incluye examen y gestión inmediata.
                    - Licencia de Motocicleta: Requiere Licencia Clase E previa. Incluye curso evaluado completo y préstamo de vehículo.

                    4. SERVICIOS EXTRAS Y REGLAS:
                    - Clases de conducción personalizadas.
                    - Cursos por Infracciones (Tickets): 4, 8 o 12 horas.
                    - Menores de 18: TLSAE online obligatorio. Deben esperar 1 año y 1 día con permiso antes del práctico.
                    - Notas Legales: Precios NO incluyen impuestos estatales. Todo examen externo debe validarse ante el DMV.

                    INSTRUCCIONES DE RESPUESTA:
                    - Responde en el idioma del usuario de forma profesional y persuasiva.
                    - Si preguntan PRECIOS: Di que varían según el caso y remite SIEMPRE al WhatsApp +1 (417) 853-2077.
                    - Sé directo con los requisitos: Deben ser originales y físicos.
                    - Finaliza invitando a escribir al WhatsApp +1 (417) 853-2077 para iniciar el trámite hoy."""
                },
                {"role": "user", "content": update.message.text}
            ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"Aviso técnico: Estamos optimizando el sistema. Por favor, contacta directamente a nuestros asesores al +1 (417) 853-2077.")

# 4. Ejecución Principal
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot de Licencias con entrenamiento actualizado iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()
