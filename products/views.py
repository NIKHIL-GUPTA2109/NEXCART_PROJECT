from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
from .models import Product
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import OrderItem
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

    user_review = None
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__is_cancelled=False
    ).exists()
        user_review = Review.objects.filter(
            user=request.user,
            product=product
        ).first()

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'reviews': reviews,
            'average_rating': average_rating,
            'review_form': ReviewForm(),
            'user_review': user_review,
            'has_purchased': has_purchased,
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

    purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__is_cancelled=False
    ).exists()

    if not purchased:

        messages.error(
            request,
            "You can review only products you have purchased."
        )

        return redirect(
            'product_detail',
            product_id
        )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review, created = Review.objects.update_or_create(

                user=request.user,

                product=product,

                defaults={

                    'rating':
                    form.cleaned_data['rating'],

                    'comment':
                    form.cleaned_data['comment']
                }
            )

            if created:

                messages.success(
                    request,
                    "Review submitted successfully."
                )

            else:

                messages.success(
                    request,
                    "Review updated successfully."
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
@login_required
def edit_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == 'POST':

        review.rating = request.POST['rating']
        review.comment = request.POST['comment']

        review.save()

        return redirect(
            'product_detail',
            product_id=review.product.id
        )

    return render(
        request,
        'products/edit_review.html',
        {
            'review': review
        }
    )
@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_id = review.product.id

    review.delete()

    return redirect(
        'product_detail',
        product_id=product_id
    )

from django.http import JsonResponse
from .models import Product


def ai_search(request):

    query = request.GET.get(
        'query',
        ''
    )

    products = Product.objects.filter(
        name__icontains=query
    )[:5]

    data = []

    for product in products:

        data.append({
            "id": product.id,
            'name': product.name,
            'price': str(product.price)
        })

    return JsonResponse(data, safe=False)

# products/views.py

from django.http import JsonResponse
from .models import Product
def ai_recommend(request):

    query = request.GET.get(
        'q',
        ''
    ).lower()

    products = Product.objects.none()

    if "gaming laptop" in query:

        products = Product.objects.filter(
            name__iregex=r"gaming|rog|legion|alienware|predator|katana|victus|blade"
        ).order_by(
            "-price"
        )[:5]

    elif "laptop" in query:

        products = Product.objects.filter(
            name__icontains="laptop"
        ).order_by(
            "-price"
        )[:5]

    elif "phone" in query or "iphone" in query:

        products = Product.objects.filter(
            name__iregex=r"iphone|oneplus|galaxy"
        )[:5]

    elif "watch" in query:

        products = Product.objects.filter(
            name__icontains="watch"
        )[:5]

    elif "headphone" in query or "headset" in query:

        products = Product.objects.filter(
            name__iregex=r"headphone|headset|airpods"
        )[:5]

    elif "speaker" in query:

        products = Product.objects.filter(
            name__icontains="jbl"
        )[:5]

    elif "book" in query:

        products = Product.objects.filter(
            category="Books"
        )[:5]

    elif "shoe" in query or "sneaker" in query:

        products = Product.objects.filter(
            name__iregex=r"nike|adidas"
        )[:5]

    else:

        products = Product.objects.order_by(
            "-price"
        )[:5]

    data = []

    for product in products:

        data.append({

            "id": product.id,
            "name": product.name,
            "price": str(product.price),
            "image": product.image.url if product.image else ""

        })

    return JsonResponse(
        data,
        safe=False
    )

