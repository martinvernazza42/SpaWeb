from .models import Cart

def cart_processor(request):
    """
    Contexto para mostrar el número de items en el carrito
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return {'cart_count': 0}
        cart = Cart.objects.filter(session_key=session_key).first()
    
    if cart:
        return {'cart_count': cart.items.count()}
    return {'cart_count': 0}

def is_admin(request):
    """
    Contexto para verificar si el usuario es administrador
    """
    return {'is_admin': request.user.is_staff}