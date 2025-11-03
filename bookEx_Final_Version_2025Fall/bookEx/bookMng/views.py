from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect

from .models import Book

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import PurchasedBook,Book



# Create your views here.

def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    books = Book.objects.all().order_by('-publishdate')

    if request.user.is_authenticated:
        owned_book_ids = PurchasedBook.objects.filter(user=request.user) \
            .values_list('book_id', flat=True)
    else:
        owned_book_ids = []

    return render(request, "bookMng/displaybooks.html", {
        "books": books,
        "owned_book_ids": owned_book_ids,
    })


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def mybooks(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    purchased_ids = PurchasedBook.objects.filter(
        user=request.user
    ).values_list("book_id", flat=True)

    books = Book.objects.filter(id__in=purchased_ids)

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })



def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })
from django.http import JsonResponse

def book_info(request, book_id):
    book = Book.objects.get(id=book_id)

    # ✅ Check if user owns the book (purchased)
    user_owns_book = PurchasedBook.objects.filter(
        user=request.user,
        book=book
    ).exists()

    return JsonResponse({
        "id": book.id,
        "name": book.name,
        "author": book.author,
        "price": str(book.price),
        "summary": book.summary,
        "username": str(book.username),
        "picture": book.picture.url if book.picture else "/static/img/placeholder_book.png",

        # ✅ Only allow delete if the user purchased it
        "can_delete": request.user.is_authenticated and user_owns_book
    })


@require_POST
@login_required
def remove_ownership(request, book_id):
    # ✅ Remove the book only from user's library (PurchasedBook table)
    PurchasedBook.objects.filter(user=request.user, book_id=book_id).delete()

    return JsonResponse({"success": True})
