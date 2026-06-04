import email

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from urllib3 import request
from django.template.loader import render_to_string
from NexCart import settings
import razorpay

from .models import (
    Order,
    OrderItem,
    ShippingAddress
)

from cart.models import (
    Cart,
    CartItem
)


client = razorpay.Client( auth=( settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET ) )

@login_required
def checkout(request):

    buy_now_product_id = request.session.get(
        'buy_now_product_id'
    )

    # =========================
    # GET REQUEST
    # =========================

    if request.method == 'GET':

        if buy_now_product_id:

            product = get_object_or_404(
                Product,
                id=buy_now_product_id
            )

            return render(
                request,
                'orders/checkout.html',
                {
                    'buy_now_product': product,
                    'total_price': product.price,
                    'cart_items': []
                }
            )

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart_items = CartItem.objects.filter(
            cart=cart
        )

        if not cart_items.exists():

            messages.error(
                request,
                "Your cart is empty."
            )

            return redirect('cart')

        total_price = sum(
            item.total_price
            for item in cart_items
        )

        return render(
            request,
            'orders/checkout.html',
            {
                'cart_items': cart_items,
                'total_price': total_price
            }
        )

    # =========================
    # SAVE SHIPPING ADDRESS
    # =========================

    shipping_address = ShippingAddress.objects.create(
        user=request.user,
        recipient_name=request.POST['recipient_name'],
        phone=request.POST['phone'],
        address=request.POST['address'],
        city=request.POST['city'],
        state=request.POST['state'],
        pincode=request.POST['pincode']
    )
    # Calculate total price before Razorpay

    if buy_now_product_id:
        product = get_object_or_404(
         Product,
        id=buy_now_product_id
        )

        total_price = product.price

    else:
        cart = get_object_or_404(
        Cart,
        user=request.user
        )

        cart_items = CartItem.objects.filter(
         cart=cart
         )

        total_price = sum(
        item.total_price
        for item in cart_items
        )
    payment_method = request.POST['payment_method']
    if payment_method !='COD':
        if payment_method in ["UPI", "CARD", "NETBANKING"]:

            payment_method = "RAZORPAY"
            amount = int(total_price * 100)

            razorpay_order = client.order.create(
            {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
            }
            )

            request.session[
            'razorpay_order_id'
            ] = razorpay_order['id']

            request.session[
          'shipping_data'
            ] = request.POST.dict()

            return render(
            request,
            'orders/payment.html',
            {
            'razorpay_order_id':
            razorpay_order['id'],

            'amount':
            amount,

            'razorpay_key':
            settings.RAZORPAY_KEY_ID
            }
        )
    # =========================
    # BUY NOW FLOW
    # =========================

    if buy_now_product_id:

        product = get_object_or_404(
            Product,
            id=buy_now_product_id
        )

        if product.stock <= 0:

            messages.error(
                request,
                "Product is out of stock."
            )

            return redirect(
                'product_detail',
                product_id=product.id
            )

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            total_price=product.price
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

        product.stock -= 1
        product.save()

        html_content = render_to_string(
    'orders/emails/order_email.html',
    {
        'username': request.user.username,
        'order': order
    }
    )

        email = EmailMultiAlternatives(
        subject=f'🎉 Order Confirmed #{order.id}',
        body='Your order has been placed.',
        from_email=settings.EMAIL_HOST_USER,
        to=[request.user.email]
     )

        email.attach_alternative(
        html_content,
         "text/html"
         )

        email.send()
        del request.session['buy_now_product_id']

        return redirect(
            'order_confirmation',
            order_id=order.id
        )

    # =========================
    # CART CHECKOUT FLOW
    # =========================

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    )

    if not cart_items.exists():

        messages.error(
            request,
            "Your cart is empty."
        )

        return redirect('cart')

    for item in cart_items:

        if item.quantity > item.product.stock:

            messages.error(
                request,
                f"Only {item.product.stock} units of {item.product.name} available."
            )

            return redirect('cart')

    total_price = sum(
        item.total_price
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        payment_method=payment_method,
        total_price=total_price
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    html_content = render_to_string(
    'orders/emails/order_email.html',
    {
        'username': request.user.username,
        'order': order
    }
)

    email = EmailMultiAlternatives(
    subject=f'🎉 Order Confirmed #{order.id}',
    body='Your order has been placed.',
    from_email=settings.EMAIL_HOST_USER,
    to=[request.user.email]
    )

    email.attach_alternative(
    html_content,
    "text/html"
    )

    email.send()

    return redirect(
        'order_confirmation',
        order_id=order.id
    )
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.all()

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'order_items': order_items
        }
    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.is_cancelled:

        messages.info(
            request,
            "This order is already cancelled."
        )

        return redirect(
            'order_detail',
            order_id=order.id
        )

    order.is_cancelled = True

    order.save()

    for item in order.items.all():

        item.product.stock += item.quantity

        item.product.save()

    
    return redirect(
        'order_detail',
        order_id=order.id
    )


@login_required
def order_confirmation(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.all()

    return render(
        request,
        'orders/order_confirmation.html',
        {
            'order': order,
            'order_items': order_items
        }
    )
@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_history.html',
        {
            'orders': orders
        }
    )
from products.models import Product

@login_required
def buy_now(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if product.stock <= 0:

        messages.error(
            request,
            "Product is out of stock."
        )

        return redirect(
            'product_detail',
            pk=product.id
        )

    request.session['buy_now_product_id'] = product.id

    return redirect('checkout')
@login_required
def payment_success(request):

    payment_id = request.GET.get(
        'payment_id'
    )

    if not payment_id:

        messages.error(
            request,
            "Payment failed."
        )

        return redirect('cart')

    buy_now_product_id = request.session.get(
        'buy_now_product_id'
    )

    shipping_data = request.session.get(
        'shipping_data'
    )

    if not shipping_data:

        messages.error(
            request,
            "Shipping information missing."
        )

        return redirect('checkout')

    shipping_address = ShippingAddress.objects.create(
        user=request.user,
        recipient_name=shipping_data['recipient_name'],
        phone=shipping_data['phone'],
        address=shipping_data['address'],
        city=shipping_data['city'],
        state=shipping_data['state'],
        pincode=shipping_data['pincode']
    )

    # =========================
    # BUY NOW FLOW
    # =========================

    if buy_now_product_id:

        product = get_object_or_404(
            Product,
            id=buy_now_product_id
        )

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method='RAZORPAY',
            total_price=product.price
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

        product.stock -= 1
        product.save()

        if 'buy_now_product_id' in request.session:
            del request.session['buy_now_product_id']

    # =========================
    # CART FLOW
    # =========================

    else:

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart_items = CartItem.objects.filter(
            cart=cart
        )

        total_price = sum(
            item.total_price
            for item in cart_items
        )

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method='RAZORPAY',
            total_price=total_price
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

    # =========================
    # EMAIL
    # =========================

    html_content = render_to_string(
    'orders/emails/order_email.html',
    {
        'username': request.user.username,
        'order': order
    }
)

    email = EmailMultiAlternatives(
    subject=f'🎉 Order Confirmed #{order.id}',
    body='Your order has been placed.',
    from_email=settings.EMAIL_HOST_USER,
    to=[request.user.email]
    )

    email.attach_alternative(
    html_content,
    "text/html"
    )

    email.send()

    

    return redirect(
        'order_confirmation',
        order_id=order.id
    )