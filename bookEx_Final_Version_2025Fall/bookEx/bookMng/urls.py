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
    path("search/", views.search_books, name="search_books"),
    path('books/<int:book_id>/rate/', views.rate_book, name='rate_book'),
    path("comment/delete/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("aboutus/", views.about, name="about"),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)