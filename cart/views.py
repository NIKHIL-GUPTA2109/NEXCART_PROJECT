from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
@login_required
def cart_page(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(
    item.product.price * item.quantity
    for item in cart_items
)
    return render(
    request,
    'cart/cart_page.html',
    {
        'cart_items': cart_items,
        'total_price': total_price
    }
)


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:

        messages.error(request,"This product is currently out of stock.")

        return redirect('product_detail',product_id=product.id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item.quantity >= product.stock:

            messages.warning(
                request,
                f"Only {product.stock} items available in stock."
            )

            return redirect('cart')

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f"{product.name} added to cart."
    )

    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):

    product = get_object_or_404(Product,id=product_id)

    cart = get_object_or_404(Cart,user=request.user)

    CartItem.objects.filter(cart=cart,product=product).delete()

    messages.success(
        request,
        f"{product.name} removed from cart."
    )

    return redirect('cart')
@login_required
def increase_quantity(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product=product
    )

    if cart_item.quantity < product.stock:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('cart')

@login_required
def decrease_quantity(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product=product
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart')