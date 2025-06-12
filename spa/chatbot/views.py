# chatbot/views.py

import json
from datetime import date

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from spa.models import Servicio, Turno

# Menú principal
MENU_TEXT = (
    "¡Hola! 👋<br>"
    "Soy tu asistente de Spa Bienestar y estoy aquí para ayudarte.<br><br>"
    "Elige una opción respondiendo con su letra:<br>"
    "A) Conocer precios de nuestros servicios<br>"
    "B) Consultar turnos disponibles<br>"
    "C) Realizar o modificar una reserva<br>"
    "D) Métodos de pago<br>"
    "E) Horario de atención y ubicación<br>"
    "F) Hablar con un asesor"
)

MENU = {
    "a": "PRECIOS_CATEGORIA",
    "b": "DISPONIBILIDAD_CATEGORIA",
    "c": "RESERVA",
    "d": "PAGO",
    "e": "INFO_HORARIO_UBICACION",
    "f": "ASESOR"
}

# Intents libres
INTENTS = {
    "saludo":        ["hola","buenos días","buen día","buenas tardes","buenas noches","qué tal","hey","holi"],
    "despedida":     ["adiós","adios","chau","chao","hasta luego","nos vemos"],
    "agradecimiento":["gracias","muchas gracias","mil gracias","te lo agradezco"],
    "reserva":       ["reserva","reservar","turno","cita"],
    "direccion":     ["ubicación","dirección","dónde estamos","localización"],
    "precio":        ["precio","cuesta","valor","tarifa"],
    "pago":          ["pago","pagos","método de pago","tarjeta","efectivo","transferencia"]
}

# Respuestas estáticas
RESPONSES = {
    "despedida":      lambda: "¡Hasta luego! Ha sido un gusto ayudarte.",
    "agradecimiento": lambda: "¡De nada! Estoy para servirte.",
    "RESERVA":        lambda: "Para reservar, ve a la sección Turnos o llámanos al 011-1234-5678.",
    "ASESOR":         lambda: "Un asesor te contactará a la brevedad. Por favor, déjanos tu nombre y teléfono.",
    "default":        lambda: "Perdona, no entendí. ¿Puedes reformular tu pregunta?"
}

@csrf_exempt
def chat(request):
    data    = json.loads(request.body.decode())
    msg     = data.get("message","").strip().lower()
    session = request.session
    state   = session.get('chat_state','NEW')

    # 1) Saludo inicial y menú
    if state == 'NEW' or any(kw in msg for kw in INTENTS['saludo']):
        session['chat_state'] = 'AWAIT_MENU'
        return JsonResponse({"reply": MENU_TEXT})

    # 2) Procesar elección de menú
    if state == 'AWAIT_MENU':
        if msg in MENU:
            flow = MENU[msg]
            session['chat_state'] = flow

            # A/B: pedir categoría con <ol> sin números manuales
            if flow in ('PRECIOS_CATEGORIA','DISPONIBILIDAD_CATEGORIA'):
                categorias = list(Servicio.objects
                                   .values_list('subcategoria__nombre', flat=True)
                                   .distinct())
                session['last_categories'] = categorias
                opts = "".join(f"<li>{c}</li>" for c in categorias)
                session['chat_state'] = flow + '_AWAIT_CAT'
                return JsonResponse({"reply":
                    f"<p>Por favor elige una categoría:</p><ol>{opts}</ol>"
                })

            # C) Reserva
            if flow == 'RESERVA':
                session['chat_state'] = 'AWAIT_MENU'
                return JsonResponse({"reply": RESPONSES['RESERVA']()})

            # D) Pago
            if flow == 'PAGO':
                session['chat_state'] = 'AWAIT_MENU'
                return JsonResponse({"reply":
                    "<p>Puedes pagar con tarjeta de crédito/débito o efectivo.<br>"
                    "Si pagas online con débito obtienes un <strong>15% de descuento</strong>.<br>"
                    "También puedes abonar presencial el día de tu turno.</p>"
                })

            # E) Horario y ubicación
            if flow == 'INFO_HORARIO_UBICACION':
                session['chat_state'] = 'AWAIT_MENU'
                return JsonResponse({"reply":
                    "<p><strong>Horario:</strong> 9 a 18 h de lunes a sábado.<br>"
                    "<strong>Ubicación:</strong> Av. Siempre Viva 123, Ciudad.</p>"
                })

            # F) Asesor
            if flow == 'ASESOR':
                session['chat_state'] = 'AWAIT_MENU'
                return JsonResponse({"reply": RESPONSES['ASESOR']()})

        return JsonResponse({"reply": "<p>Opción no válida.</p>" + MENU_TEXT})

    # 3) A-1) Selección de categoría para precios
    if state == 'PRECIOS_CATEGORIA_AWAIT_CAT':
        try:
            idx = int(msg) - 1
            cat = session['last_categories'][idx]
        except:
            return JsonResponse({"reply":"<p>Selección inválida. Envía el número correcto.</p>"})
        servicios = Servicio.objects.filter(subcategoria__nombre__iexact=cat)
        lines = "".join(f"<li>{s.nombre}: <strong>${s.precio}</strong></li>" for s in servicios)
        session['chat_state'] = 'AWAIT_MENU'
        return JsonResponse({"reply":
            f"<p>Servicios en categoría <em>{cat}</em>:</p><ul>{lines}</ul>"
        })

    # 4) B-1) Selección de categoría para disponibilidad
    if state == 'DISPONIBILIDAD_CATEGORIA_AWAIT_CAT':
        try:
            idx = int(msg) - 1
            cat = session['last_categories'][idx]
        except:
            return JsonResponse({"reply":"<p>Selección inválida. Envía el número correcto.</p>"})
        servicios = Servicio.objects.filter(subcategoria__nombre__iexact=cat)
        session['last_services'] = [s.id for s in servicios]
        opts = "".join(f"<li>{s.nombre}</li>" for s in servicios)
        session['chat_state'] = 'DISPONIBILIDAD_AWAIT_SVC'
        return JsonResponse({"reply":
            "<p>Selecciona el servicio para ver turnos disponibles:</p><ol>" + opts + "</ol>"
        })

    # 5) B-2) Mostrar disponibilidades no reservadas
    if state == 'DISPONIBILIDAD_AWAIT_SVC':
        try:
            idx = int(msg) - 1
            svc_id = session['last_services'][idx]
            servicio = Servicio.objects.get(id=svc_id)
        except:
            return JsonResponse({"reply":"<p>Selección inválida. Envía el número correcto.</p>"})

        disponibilidad = {}
        for disp in servicio.disponibilidades.all():
            f = disp.fecha
            start = disp.hora_inicio
            end   = disp.hora_fin
            if not Turno.objects.filter(servicio=servicio, fecha=f, hora=start).exists():
                fecha_s = f.strftime('%d/%m/%Y')
                slot = f"{start.strftime('%H:%M')} – {end.strftime('%H:%M')}"
                disponibilidad.setdefault(fecha_s, []).append(slot)

        if disponibilidad:
            items = "".join(f"<li><strong>{d}</strong>: {', '.join(slots)}</li>"
                             for d,slots in disponibilidad.items())
            reply = f"<p>Turnos disponibles para <em>{servicio.nombre}</em>:</p><ul>{items}</ul>"
        else:
            reply = f"<p>No hay turnos disponibles para <em>{servicio.nombre}</em>.</p>"

        session['chat_state'] = 'AWAIT_MENU'
        return JsonResponse({"reply": reply})

    # 6) Fallback: intents libres y precio dinámico
    for intent, keywords in INTENTS.items():
        if any(kw in msg for kw in keywords):
            if intent in ('despedida','agradecimiento','reserva','direccion','pago'):
                key = intent.upper() if intent=='reserva' else intent
                return JsonResponse({"reply": RESPONSES.get(key, RESPONSES['default'])()})
            if intent == 'precio':
                encontrado = next(
                    (s for s in Servicio.objects.all() if s.nombre.lower() in msg), None
                )
                if encontrado:
                    return JsonResponse({"reply":
                        f"<p>El precio de <strong>{encontrado.nombre}</strong> es <strong>${encontrado.precio}</strong>.</p>"
                    })
                return JsonResponse({"reply":"<p>¿De qué servicio deseas saber el precio?</p>"})

    # 7) Por defecto
    return JsonResponse({"reply": RESPONSES['default']()})
