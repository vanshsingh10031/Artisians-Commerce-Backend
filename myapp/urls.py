from django.urls import path
from .views import UsersList,UserDetail,UserLogin,UserRegistration,register_artisan,dashboard_data,PlaceOrder   
from . import views
from myapp.ProductList import analyze_product_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/<int:userid>/', UserDetail.as_view(), name='user-detail'),  # New route
    path('login/', UserLogin.as_view(), name='user-login'),
    # Customer APIs

    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("view-cart/<int:user_id>/", views.view_cart, name="view-cart"),
    path("remove-from-cart/", views.remove_from_cart, name="remove-from-cart"),
    path("all-products/", views.get_all_products, name="get_all_products"),
    path('register/', UserRegistration.as_view, name='register'),
    path("products/user/<int:userid>/product/<int:productid>/update/", views.update_product, name="update_product"),
    path("products/<int:userid>/<int:productid>/", views.delete_product, name="delete_product"),
     # ---- DASHBOARD ----
    path("dashboard/<int:userid>/", dashboard_data, name="dashboard-data"),
      # New product paths
      # New: Create product
    path('products/user/<int:userid>/create/', views.create_product, name='create_product'),
    path('products/user/<int:userid>/', views.get_products_by_user, name='get_products_by_user'),
    path('analyze-image/', analyze_product_image, name='analyze_image'),
    path('register-artisan/', register_artisan, name='register-artisan'),

      # ---- ORDERS ----
    path("place-order/<int:userid>/", PlaceOrder.as_view(), name="PlaceOrder"),  # 👈 NEW URL
    path('products/user/<int:userid>/product/<int:productid>/', views.get_product_detail, name='get_product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)