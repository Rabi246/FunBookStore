from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order, OrderItem, MainMenu
from .cart import add_to_cart, remove_from_cart, cart_items, cart_total, clear_cart
from .models import PurchasedBook, Book

def cart_detail(request):
    items = cart_items(request.session)
    total = cart_total(request.session)
    return render(
        request,
        "bookMng/cart.html",
        {"items": items, "total": total, "item_list": MainMenu.objects.all()},
    )

def cart_add(request, book_id):
    qty = int(request.POST.get("quantity", 1)) if request.method == "POST" else 1
    add_to_cart(request.session, book_id, qty)
    return redirect("bookMng:cart_detail")

def cart_remove(request, book_id):
    remove_from_cart(request.session, book_id)
    return redirect("bookMng:cart_detail")

@login_required
def checkout(request):
    items = cart_items(request.session)
    if not items:
        return redirect("bookMng:cart_detail")

    total = cart_total(request.session)

    for it in items:
        PurchasedBook.objects.get_or_create(user=request.user, book=it["book"])

    clear_cart(request.session)
    return render(request, "bookMng/checkout_success.html", {"total": total})

@login_required
def purchases(request):
    paid_orders = request.user.orders.filter(paid=True).prefetch_related("items__book")
    unique = {}
    for order in paid_orders:
        for item in order.items.all():
            unique[item.book.id] = item.book
    books = list(unique.values())
    return render(request, "bookMng/purchases.html", {"books": books})

@login_required
def my_books(request):
    purchased_ids = PurchasedBook.objects.filter(
        user=request.user
    ).values_list("book_id", flat=True)

    books = Book.objects.filter(id__in=purchased_ids)
    return render(request, "bookMng/mybooks.html", {"books": books})