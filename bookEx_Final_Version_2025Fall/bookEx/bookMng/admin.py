from django.contrib import admin

# Register your models here.
from .models import MainMenu, PurchasedBook
from .models import Book
from .models import Comment


admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(Comment)


from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "paid", "created_at")
    list_filter = ("paid", "created_at")
    inlines = [OrderItemInline]

@admin.register(PurchasedBook)
class PurchasedBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "purchased_at")
    search_fields = ("user__username", "book__name")