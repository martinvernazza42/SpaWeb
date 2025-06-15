from django import template

register = template.Library()

@register.filter
def has_attr(obj, attr_name):
    """Verifica si un objeto tiene un atributo específico"""
    return hasattr(obj, attr_name)

@register.filter
def get_cart_count(request):
    """Obtiene el número de items en el carrito"""
    from ..models import Cart
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return 0
        cart = Cart.objects.filter(session_key=session_key).first()
    
    if cart:
        return cart.items.count()
    return 0