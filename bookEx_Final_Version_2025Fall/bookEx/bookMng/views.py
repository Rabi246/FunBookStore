from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import MainMenu, Book, PurchasedBook, Comment, Rating
from .forms import BookForm, RegisterForm, CommentForm

# Create your views here.

def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })

def postbook(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    books = Book.objects.all().order_by('-publishdate')

    owned_book_ids = PurchasedBook.objects.filter(user=request.user)\
                        .values_list('book_id', flat=True)

    return render(request, "bookMng/displaybooks.html", {
        "books": books,
        "owned_book_ids": owned_book_ids,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.pic_path = book.picture.url[14:] if book.picture else ''
    comments = book.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('bookMng:book_detail', book_id=book.id)
    else:
        form = CommentForm()

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comments': comments,
        'form': form,
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
    for b in books:
        b.pic_path = b.picture.url[14:]
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

def book_info(request, book_id):
    book = Book.objects.get(id=book_id)
    user_owns_book = PurchasedBook.objects.filter(
        user=request.user,
        book=book
    ).exists()

    # Get the user's rating for this book, if any
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(user=request.user, book=book).value
        except Rating.DoesNotExist:
            user_rating = None

    return JsonResponse({
        "id": book.id,
        "name": book.name,
        "author": book.author,
        "price": str(book.price),
        "summary": book.summary,
        "username": str(book.username),
        "picture": book.picture.url if book.picture else "/static/img/placeholder_book.png",
        "can_delete": request.user.is_authenticated and user_owns_book,
        "user_rating": user_rating    # <-- this is key!
    })

@require_POST
@login_required
def remove_ownership(request, book_id):
    PurchasedBook.objects.filter(user=request.user, book_id=book_id).delete()
    return JsonResponse({"success": True})

def about(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return render(request, "bookMng/aboutus.html", {
        "item_list": MainMenu.objects.all()
    })

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('mybooks')
    return redirect('login')

def search_books(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Book.objects.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query)
        ).distinct()

    return render(request, "bookMng/search_results.html", {
        "query": query,
        "results": results,
        "item_list": MainMenu.objects.all()
    })

@require_POST
@login_required
def rate_book(request, book_id):
    """Create or update the user's rating for a specific book."""
    book = get_object_or_404(Book, id=book_id)

    try:
        value = int(request.POST.get('value', ''))
        if value < 1 or value > 5:
            raise ValueError()
    except ValueError:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': 'Rating must be between 1 and 5.'}, status=400)
        messages.error(request, 'Please choose a rating from 1 to 5.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    Rating.objects.update_or_create(
        book=book,
        user=request.user,
        defaults={'value': value}
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'value': value})

    messages.success(request, f'Your rating ({value}★) has been saved!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(request.META.get("HTTP_REFERER", "/"))
