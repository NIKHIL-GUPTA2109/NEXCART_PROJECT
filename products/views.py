from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
from .models import Product
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def product_list(request):

    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    sort_by = request.GET.get('sort')

    if sort_by == 'low':
        products = products.order_by('price')

    elif sort_by == 'high':
        products = products.order_by('-price')

    elif sort_by == 'new':
        products = products.order_by('-created_at')
  
    return render(
        request,
        'products/product_list.html',
        {
            'products': products
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )
    reviews = Review.objects.filter(
    product=product
).select_related('user')
    average_rating = Review.objects.filter(
    product=product
).aggregate(
    Avg('rating')
)['rating__avg']
    return render(
        request,
        'products/product_detail.html',
        {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': ReviewForm()
        }
    )


@login_required
def add_review(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            Review.objects.update_or_create(

                user=request.user,

                product=product,

                defaults={

                    'rating':
                    form.cleaned_data['rating'],

                    'comment':
                    form.cleaned_data['comment']
                }
            )

    return redirect(
        'product_detail',
        product_id
    )
def category_products(
    request,
    category
):

    products = Product.objects.filter(
        category=category
    )

    return render(
        request,
        'products/category_products.html',
        {
            'products': products,
            'category': category
        }
    )