from decimal import Decimal

from django.conf import settings

from django.contrib.auth.models import User
from django.db import models

from django.db.models import Avg

# Create your models here.
class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    summary = models.TextField()
    picture = models.FileField(upload_to='uploads/', blank=True, null=True)


    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    publishdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name





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


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.book}"

class Rating(models.Model):
    book = models.ForeignKey('Book', related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='book_ratings', on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user')  # one rating per user per book

    def __str__(self):
        return f'{self.user} → {self.book} [{self.value}]'



