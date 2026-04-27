from django.db.models import Sum

def cart_context(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = request.user.cart_items.aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_count':cart_count}