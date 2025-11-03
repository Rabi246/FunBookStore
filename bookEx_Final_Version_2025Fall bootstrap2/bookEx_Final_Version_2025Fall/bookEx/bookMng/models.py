from decimal import Decimal

from django.conf import settings

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)





class Order(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
        created_at = models.DateTimeField(auto_now_add=True)
        total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
        paid = models.BooleanField(default=False)

        def __str__(self):
            return f"Order #{self.id} by {self.user} on {self.created_at:%Y-%m-%d}"

class OrderItem(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
        book = models.ForeignKey(Book, on_delete=models.PROTECT)
        quantity = models.PositiveIntegerField(default=1)
        unit_price = models.DecimalField(max_digits=8, decimal_places=2)
        line_total = models.DecimalField(max_digits=10, decimal_places=2)

        def __str__(self):
            return f"{self.quantity} × {self.book.title}"

class PurchasedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchased_books")
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")