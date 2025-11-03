from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import views_cart

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path("cart/", views_cart.cart_detail, name="cart_detail"),
    path("cart/add/<int:book_id>/", views_cart.cart_add, name="cart_add"),
    path("cart/remove/<int:book_id>/", views_cart.cart_remove, name="cart_remove"),
    path("checkout/", views_cart.checkout, name="checkout"),
    path("purchases/", views_cart.my_books, name="purchases"),
    path("book-info/<int:book_id>/", views.book_info, name="book_info"),
    path("remove-book/<int:book_id>/", views.remove_ownership, name="remove_ownership"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)