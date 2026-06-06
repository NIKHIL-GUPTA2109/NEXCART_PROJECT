from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from products.models import Product, Review
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from wishlist.models import Wishlist
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            try:
                html_content = render_to_string(
                    'emails/welcome_email.html',
                    {'user': user}
                )

                email = EmailMultiAlternatives(
                    subject='🎉 Welcome To NexCart',
                    body='Welcome To NexCart',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email]
                )

                email.attach_alternative(
                    html_content,
                    "text/html"
                )

                email.send()
            
            except Exception as e:
                print(f"Email Error: {e}")

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
    
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
