from decimal import Decimal
from .models import Book

CART_SESSION_KEY = "cart"  # {'book_id': quantity}

def get_cart(session):
    return session.get(CART_SESSION_KEY, {})

def save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True

def add_to_cart(session, book_id, qty=1):
    cart = get_cart(session)
    cart[str(book_id)] = cart.get(str(book_id), 0) + int(qty)
    if cart[str(book_id)] <= 0:
        cart.pop(str(book_id), None)
    save_cart(session, cart)

def remove_from_cart(session, book_id):
    cart = get_cart(session)
    cart.pop(str(book_id), None)
    save_cart(session, cart)

def clear_cart(session):
    save_cart(session, {})

def cart_items(session):
    cart = get_cart(session)
    ids = [int(i) for i in cart.keys()]
    books = Book.objects.filter(id__in=ids)
    items = []
    for b in books:
        q = int(cart.get(str(b.id), 0))
        if q > 0:
            unit_price = b.price
            line_total = (unit_price * Decimal(q)).quantize(Decimal("0.01"))
            items.append({
                "book": b,
                "quantity": q,
                "unit_price": unit_price,
                "line_total": line_total
            })
    return items

def cart_total(session):
    total = Decimal("0.00")
    for it in cart_items(session):
        total += it["line_total"]
    return total.quantize(Decimal("0.01"))
