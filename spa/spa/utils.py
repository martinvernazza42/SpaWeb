from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def render_to_pdf(template_src, context_dict={}):
    """
    Renderiza una plantilla HTML a un archivo PDF
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Crear PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None