from django.urls import path
from .import views
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path(
    'review/<int:product_id>/',
    views.add_review,
    name='add_review'
),
path(
    'review/edit/<int:review_id>/',
    views.edit_review,
    name='edit_review'
),
path(
    'review/delete/<int:review_id>/',
    views.delete_review,
    name='delete_review'
),
path(
    'category/<str:category>/',
    views.category_products,
    name='category_products'
),
]
