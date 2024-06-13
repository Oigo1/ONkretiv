from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ONkretiv/', views.ONkretiv, name='ONkretiv'),
    path('products/<str:category_type>/<str:category_name>/', views.products_by_category, name='products_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('company/', views.company, name='company'),


    # path('products/<str:category_name>/', views.products_by_category, name='products_by_category'),
    path('shoes/', views.shoes, name='shoes'),
    path('pants/', views.pants, name='pants'),
    path('tshirt/', views.tshirt, name='tshirt'),
    path('jackets/', views.jackets, name='jackets'),
    path('limited/', views.limited, name='limited'),
    path('discount/', views.discount, name='discount'),
    path('login/', views.login, name='login'),
    path('launch/', views.launch, name='launch'),
    path('creative/', views.creative, name='creative'),
    
]