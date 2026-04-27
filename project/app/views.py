from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from app.forms import CustomUserCreationForm
from app.models import Product,CartItem,Order, OrderItem

class Register(View):
    template_name = 'registration/register.html'

    def get(self,request):
        context = {
            "form":CustomUserCreationForm()
        }
        return render(request,self.template_name,context)
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
        context = {
            'form':form
        }
        return render(request,self.template_name,context)
@login_required
def index(request):
    products = Product.objects.prefetch_related('images').all()
    return render(request,'product/index.html',{"products":products})
@login_required
def cart(request):
    cart_items = request.user.cart_items.select_related('product').all()
    cart_items_with_total = []
    for item in cart_items:
        item.total = item.product.price * item.quantity
        cart_items_with_total.append(item)
    total_price = sum(item.total for item in cart_items_with_total)
    return render(request,'cart/index.html',{
        'cart_items':cart_items_with_total,
        'total_price':total_price
    })
@login_required
def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart_item,created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request,f'Товар{product.name} добавлен в корзину')
    return redirect('product')
@login_required
def cart_index(request):
    cart_items = request.user.cart_items.select_related('product').all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'cart/index.html',{'cart_items':cart_items,'total_price':total_price})
@login_required
def increase_quantity(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart_item = get_object_or_404(CartItem, user=request.user, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return render('cart')
@login_required
@transaction.atomic
def create_order(request):
    cart_items = request.user.cart_items.select_related('product').all()
    if not cart_items:
        messages.error('Невозможно оформить заказ. Ваша корзина пуста')
        return redirect('cart')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        status='pending',
        total_price=total_price,
        shipping_adress='Адрес'
    )

    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    cart_items.delete()
    messages.success(request,f'Заказ {order.id} оформлен успешно')
    return redirect('order_succes',order_id=order.id)
def order_succes(request,order_id):
    return render(request,'order/succes.html',{'order_id':order_id})    