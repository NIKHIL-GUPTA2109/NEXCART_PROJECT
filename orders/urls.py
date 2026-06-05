from django.urls import path
from .import views
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/',views.order_history,name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path(
    'payment-success/',
    views.payment_success,
    name='payment_success'
),
path("contact-us/", views.contact_us, name="contact_us"),
]