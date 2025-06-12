# spa/context_processors.py

from .models import Cart

def cart_count(request):
    session_key = request.session.session_key or request.session.create()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=session_key).first()
    count = cart.items.count() if cart else 0
    return {'cart_count': count}

