from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from products.models import Product, Review
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from wishlist.models import Wishlist
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from utils.email_service import send_welcome_email
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import (
    urlsafe_base64_encode
)

from django.utils.encoding import (
    force_bytes
)

from utils.email_service import (
    send_password_reset_email
)
# Create your views here.
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            try:

                send_welcome_email(
                    user.email,
                    user.username
                )

            except Exception as e:
                print(f"EMAIL ERROR: {e}")

            messages.success(
                request,
                f"🎉 Thank you for registering with NexCart, {user.username}! Your account has been created successfully."
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )
    
def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            return render(request,'login.html',{'error': 'Invalid Username or Password'})
        
    return render(request,'login.html')
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
   
    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    else:
        products = Product.objects.filter(is_featured=True)[:16]
        
    return render(
        request,
        'home.html',
        {'products': products, 'search': search}
    )
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    order_count=Order.objects.filter(user=request.user).count()
    review_count=Review.objects.filter(user=request.user).count()
    wishlist_count=Wishlist.objects.filter(user=request.user).count()
    return render(
        request,
        'profile.html',
        {
            'order_count': order_count,
            'review_count': review_count,
            'wishlist_count': wishlist_count
        }
    )


def password_reset_request(request):

    if request.method == "POST":

        email = request.POST.get(
            "email"
        )

        user = User.objects.filter(
            email=email
        ).first()

        if user:

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = (
                default_token_generator
                .make_token(user)
            )

            reset_link = (
                f"{request.scheme}://"
                f"{request.get_host()}"
                f"{reverse('password_reset_confirm', kwargs={
                    'uidb64': uid,
                    'token': token
                })}"
            )

            try:

                send_password_reset_email(
                    user,
                    reset_link
                )

                print(
                    "PASSWORD RESET EMAIL SENT"
                )

            except Exception as e:

                print(
                    f"PASSWORD RESET ERROR: {e}"
                )

        return redirect(
            'password_reset_done'
        )

    return render(
        request,
        'registration/password_reset_form.html'
    )