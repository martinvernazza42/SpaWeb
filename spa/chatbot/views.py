# chatbot/views.py

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Importar el chatbot gratuito
from .free_chatbot import get_free_chatbot_response

@csrf_exempt
def chat(request):
    """Vista para manejar las solicitudes de chat"""
    data = json.loads(request.body.decode())
    message = data.get("message", "").strip()
    session = request.session
    
    # Inicializar el historial de chat si no existe
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # Obtener el historial de chat
    chat_history = session['chat_history']
    
    # Limitar el historial a las últimas 10 interacciones
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
    
    # Usar el chatbot gratuito
    reply = get_free_chatbot_response(message, chat_history)
    
    # Actualizar el historial de chat
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": reply})
    session['chat_history'] = chat_history
    
    # Agregar botones de sugerencia según el contexto
    if "precio" in message.lower() or "costo" in message.lower() or "cuanto" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Cuánto cuesta un masaje relajante?</button><button class="suggestion-btn">¿Precio de limpieza facial?</button><button class="suggestion-btn">¿Cuánto vale la exfoliación?</button></div>'
    
    elif "reserva" in message.lower() or "turno" in message.lower() or "cita" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Cómo reservo un turno?</button><button class="suggestion-btn">¿Cuál es el horario de atención?</button><button class="suggestion-btn">¿Hay descuentos en reservas?</button></div>'
    
    elif "hola" in message.lower() or message.lower() in ["hi", "hey", "buenos dias", "buenas tardes"]:
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Qué servicios ofrecen?</button><button class="suggestion-btn">¿Dónde están ubicados?</button><button class="suggestion-btn">¿Cuáles son los horarios?</button></div>'
    
    elif "masaje" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Cuánto cuesta el masaje relajante?</button><button class="suggestion-btn">¿Qué incluye el masaje terapéutico?</button><button class="suggestion-btn">¿Duración del masaje con piedras?</button></div>'
    
    elif "facial" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Precio de limpieza facial?</button><button class="suggestion-btn">¿En qué consiste el tratamiento hidratante?</button><button class="suggestion-btn">¿Para qué sirve el tratamiento antiedad?</button></div>'
    
    elif "corporal" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Qué es la exfoliación corporal?</button><button class="suggestion-btn">¿Precio de la envoltura corporal?</button><button class="suggestion-btn">¿Beneficios del drenaje linfático?</button></div>'
    
    elif "ubicacion" in message.lower() or "direccion" in message.lower() or "donde" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Cómo llego al spa?</button><button class="suggestion-btn">¿Tienen estacionamiento?</button><button class="suggestion-btn">¿Están abiertos los sábados?</button></div>'
    
    elif "pago" in message.lower() or "descuento" in message.lower():
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Aceptan tarjetas?</button><button class="suggestion-btn">¿Hay descuentos?</button><button class="suggestion-btn">¿Se puede pagar en efectivo?</button></div>'
    
    else:
        # Sugerencias por defecto para cualquier otra consulta
        reply += '<div class="suggestions-container"><button class="suggestion-btn">¿Qué servicios ofrecen?</button><button class="suggestion-btn">¿Cuáles son los horarios?</button><button class="suggestion-btn">¿Cómo reservo un turno?</button></div>'
    
    return JsonResponse({"reply": reply})