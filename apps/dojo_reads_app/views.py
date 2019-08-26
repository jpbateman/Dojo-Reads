from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Review, Author
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'dojo_reads_app/index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pass_to_hash = request.POST['password']
            hashed_pass = bcrypt.hashpw(pass_to_hash.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pass)
            request.session["user_id"] = new_user.id
            return redirect('/')

def login(request):
    print('hi')
    print(request.POST)
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        form = request.POST
        try:
            print('trying...')
            user = User.objects.get(email=form["email"])
        except:
            print('no success')
            messages.error(request, "Check your email and password!")
            return redirect("/")
        if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
            print('passwords matched')
            request.session["user_id"] = user.id
            return redirect('/books')
            messages.error(request, "Check your email and password!")
        print('no match')
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')

def books(request):
    if "user_id" not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    reviews = Review.objects.all().order_by('-id')[:3]
    books = Book.objects.all()
    context = {
        'user': user,
        'reviews': reviews,
        'books': books,
    }
    return render(request, 'dojo_reads_app/books.html', context)

def add(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    return render(request, 'dojo_reads_app/add.html', {'books': books, 'authors': authors})

def create(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        form = request.POST
        user = User.objects.get(id=request.session['user_id'])
        if form['title_list']=="Select Here":
            book = Book.objects.create(title=form['book_title'])
        else: 
            book = Book.objects.get(title=form['title_list'])
        if form['author_list']=="Select Here":
            author = Author.objects.create(name=form['book_author'])
            book.authors.add(author)
        else:
            author = Author.objects.get(name=form["author_list"])
            book.authors.add(author)
        new_review = Review.objects.create(review=form['review'], rating=form['rating'], user=user, book=book)
    return redirect('/books')

def display(request, id):
    form = request.POST
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    author = Author.objects.get(books__id=id)
    reviews = Review.objects.filter(book=book)
    context = {
        "book": book,
        "author": author,
        "reviews": reviews,
        "user": user,
    }
    return render(request, 'dojo_reads_app/bookinfo.html', context)

def delete(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        del_review = Review.objects.get(id=request.POST['delete'])
        del_review.delete()
    return redirect('/books')

def user(request, id):
    form = request.POST
    user = User.objects.get(id=id)
    total = 0
    reviews = Review.objects.filter(user__id=id)
    for review in reviews:
        total += 1

    print(reviews)
    context = {
        "user": user,
        "reviews": reviews,
        "total": total,
    }
    return render(request, 'dojo_reads_app/users.html', context)


