import re
from django.core.cache import cache

# Base de conocimiento del spa
SPA_INFO = {
    "nombre": "Spa Bienestar",
    "direccion": "French 414, Resistencia, Chaco",
    "telefono": "(011) 4567-8900",
    "horario": "Lunes a viernes de 9:00 a 20:00 y sábados de 10:00 a 18:00. Domingos cerrado.",
    "pagos": "Efectivo, tarjetas de crédito/débito y transferencias bancarias. 15% de descuento pagando con débito 48hs antes.",
    "descuento": "15% pagando con débito con 48 horas de anticipación",
    "reserva": "Desde la sección de servicios en nuestra web o llamando al (011) 4567-8900",
    "estacionamiento": "Sí, contamos con estacionamiento gratuito para nuestros clientes."
}

# Servicios y precios
SERVICIOS = {
    "masajes": {
        "relajante": {"precio": 8000, "duracion": "60 minutos", "descripcion": "Masaje suave para aliviar el estrés y la tensión muscular."},
        "terapeutico": {"precio": 12000, "duracion": "60 minutos", "descripcion": "Masaje profundo para tratar dolores musculares y mejorar la movilidad."},
        "piedras": {"precio": 15000, "duracion": "90 minutos", "descripcion": "Masaje con piedras calientes que ayuda a relajar los músculos profundos."},
        "deportivo": {"precio": 10000, "duracion": "60 minutos", "descripcion": "Masaje intenso para deportistas, ayuda en la recuperación muscular."}
    },
    "faciales": {
        "limpieza": {"precio": 7500, "duracion": "45 minutos", "descripcion": "Limpieza facial profunda para eliminar impurezas y células muertas."},
        "hidratante": {"precio": 9000, "duracion": "60 minutos", "descripcion": "Tratamiento hidratante para pieles secas o deshidratadas."},
        "antiedad": {"precio": 15000, "duracion": "75 minutos", "descripcion": "Tratamiento para reducir líneas de expresión y mejorar la elasticidad."}
    },
    "corporales": {
        "exfoliacion": {"precio": 10000, "duracion": "45 minutos", "descripcion": "Exfoliación corporal para eliminar células muertas y renovar la piel."},
        "envoltura": {"precio": 18000, "duracion": "90 minutos", "descripcion": "Envoltura corporal con productos naturales para hidratar y desintoxicar."},
        "drenaje": {"precio": 12000, "duracion": "60 minutos", "descripcion": "Drenaje linfático para reducir la retención de líquidos."}
    }
}

def get_free_chatbot_response(message, context=None):
    """
    Genera una respuesta basada en reglas y la base de conocimiento
    """
    message = message.lower().strip()
    
    # Verificar caché primero
    cache_key = f"free_chat_{hash(message)}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    
    # Saludos
    if re.search(r'\b(hola|buenos dias|buenas tardes|buenas noches|hey|hi|hello)\b', message):
        response = f"¡Hola! Soy el asistente virtual de {SPA_INFO['nombre']}. Puedo ayudarte con información sobre nuestros servicios, precios, horarios o reservas. ¿Qué te gustaría saber?"
    
    # Despedidas
    elif re.search(r'\b(adios|chau|hasta luego|nos vemos|bye)\b', message):
        response = "¡Hasta pronto! Esperamos verte en nuestro spa. Si tienes más preguntas, no dudes en escribirme."
    
    # Agradecimientos
    elif re.search(r'\b(gracias|te agradezco|thanks)\b', message):
        response = "¡De nada! Estoy aquí para ayudarte. ¿Hay algo más que quieras saber sobre nuestros servicios?"
    
    # Horarios
    elif re.search(r'\b(horario|hora|cuando|abierto|cerrado|atienden|sabado|domingo)\b', message):
        response = f"Nuestro horario de atención es: {SPA_INFO['horario']}"
    
    # Ubicación y estacionamiento
    elif re.search(r'\b(donde|ubicacion|direccion|lugar|como llego|estacionamiento|parking)\b', message):
        if "estacionamiento" in message or "parking" in message:
            response = SPA_INFO['estacionamiento']
        else:
            response = f"Estamos ubicados en {SPA_INFO['direccion']}. {SPA_INFO['estacionamiento']} Puedes encontrarnos fácilmente en Google Maps buscando '{SPA_INFO['nombre']}'."
    
    # Pagos y descuentos
    elif re.search(r'\b(pago|pagar|tarjeta|efectivo|transferencia|descuento)\b', message):
        if "descuento" in message:
            response = f"Ofrecemos un {SPA_INFO['descuento']}."
        else:
            response = f"Aceptamos {SPA_INFO['pagos']}"
    
    # Reservas
    elif re.search(r'\b(reserva|turno|cita|agendar|programar)\b', message):
        response = f"Para reservar un turno puedes hacerlo {SPA_INFO['reserva']}."
    
    # Servicios específicos
    elif "masaje" in message:
        if "relajante" in message:
            info = SERVICIOS["masajes"]["relajante"]
            response = f"El masaje relajante cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "terapeutico" in message or "terapéutico" in message:
            info = SERVICIOS["masajes"]["terapeutico"]
            response = f"El masaje terapéutico cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "piedra" in message:
            info = SERVICIOS["masajes"]["piedras"]
            response = f"El masaje con piedras calientes cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "deportivo" in message:
            info = SERVICIOS["masajes"]["deportivo"]
            response = f"El masaje deportivo cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        else:
            response = "Ofrecemos varios tipos de masajes: relajante ($8,000, 60 min), terapéutico ($12,000, 60 min), con piedras calientes ($15,000, 90 min) y deportivo ($10,000, 60 min). ¿Sobre cuál te gustaría más información?"
    
    elif "facial" in message:
        if "limpieza" in message:
            info = SERVICIOS["faciales"]["limpieza"]
            response = f"La limpieza facial cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "hidratante" in message or "hidratacion" in message:
            info = SERVICIOS["faciales"]["hidratante"]
            response = f"El tratamiento facial hidratante cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "antiedad" in message or "anti-edad" in message or "arrugas" in message:
            info = SERVICIOS["faciales"]["antiedad"]
            response = f"El tratamiento facial antiedad cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        else:
            response = "Ofrecemos varios tratamientos faciales: limpieza ($7,500, 45 min), hidratante ($9,000, 60 min) y antiedad ($15,000, 75 min). ¿Sobre cuál te gustaría más información?"
    
    elif "corporal" in message:
        if "exfoliacion" in message or "exfoliar" in message:
            info = SERVICIOS["corporales"]["exfoliacion"]
            response = f"La exfoliación corporal cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "envoltura" in message:
            info = SERVICIOS["corporales"]["envoltura"]
            response = f"La envoltura corporal cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        elif "drenaje" in message or "linfatico" in message:
            info = SERVICIOS["corporales"]["drenaje"]
            response = f"El drenaje linfático cuesta ${info['precio']}, dura {info['duracion']}. {info['descripcion']}"
        else:
            response = "Ofrecemos varios tratamientos corporales: exfoliación ($10,000, 45 min), envoltura ($18,000, 90 min) y drenaje linfático ($12,000, 60 min). ¿Sobre cuál te gustaría más información?"
    
    # Servicios generales
    elif re.search(r'\b(servicio|tratamiento|ofrecen|tienen)\b', message):
        response = "Ofrecemos tres categorías principales de servicios:\n\n1. Masajes: relajante, terapéutico, con piedras calientes y deportivo.\n2. Tratamientos faciales: limpieza, hidratante y antiedad.\n3. Tratamientos corporales: exfoliación, envoltura y drenaje linfático.\n\n¿Sobre qué categoría te gustaría más información?"
    
    # Precios generales
    elif re.search(r'\b(precio|costo|valor|cuanto)\b', message):
        response = "Los precios de nuestros servicios varían según el tratamiento:\n\n• Masajes: desde $8,000 hasta $15,000\n• Faciales: desde $7,500 hasta $15,000\n• Corporales: desde $10,000 hasta $18,000\n\n¿Sobre qué servicio específico te gustaría saber el precio?"
    
    # Respuesta por defecto
    else:
        response = "Puedo ayudarte con información sobre:\n\n• Nuestros servicios y precios\n• Horarios de atención\n• Ubicación y estacionamiento\n• Reservas y turnos\n• Métodos de pago y descuentos\n\n¿Qué te gustaría saber?"
    
    # Guardar en caché
    cache.set(cache_key, response, 3600 * 24)  # 24 horas
    
    return response