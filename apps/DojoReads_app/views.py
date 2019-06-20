from django.shortcuts import render, HttpResponse, redirect
from .models import User, Book, Review, Reg_Manager, Author
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    # return render(request,'index.html')
    return render(request,'index.html')

def register(request):
    print("Errors include:")       
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.warning(request,value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST["pw"].encode(),bcrypt.gensalt())
        print(hashedpw)
        User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email = request.POST["email"],password = hashedpw)
        request.session["id"]= User.objects.last().id
        return redirect('/books')
    
def success(request):
    print('in success')
    if not "id" in request.session:
        return redirect('/')
    else:
        print(request.session["id"])
        context={
            'user': User.objects.get(id=request.session["id"]),
            'reviews' : Review.objects.all().order_by('-id')[:5],
            'books' : Book.objects.all()
        }
        return render(request,'home.html',context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session["id"] = User.objects.get(email = request.POST["email"]).id
    return redirect('/books')

def logout(request):
    del request.session["id"]
    return redirect('/')

#home page with recent book reviews, and other books with reviews

#add book with review
def add(request):
    context={
        "authors" : Author.objects.all()
    }
    print(Author.objects.all())
    return render(request,"add.html",context)

def add_book_review(request):
    print(request.session["id"])
    print(request.POST)
    user = User.objects.get(id = request.session["id"])
    if (len(request.POST["new_author"])>1):
        author = Author.objects.create(name=request.POST["new_author"])
    else:
        author = Author.objects.get(id = request.POST["authors_dropdown"])
    book = Book.objects.create(title=request.POST["title"], author = author)
    book_id = Book.objects.last().id
    review = Review.objects.create(review=request.POST["review"],rating=request.POST["rating"],book = book, user = user)
    book.reviews.add(review)
    user.reviewcount = 1 
    user.save()
    return redirect('/books/'+str(book_id))

# book page with reviews and add book review for 
def book_page(request,book_id):
    context = {
        'book' :Book.objects.get(id = book_id),
        'reviews' :Book.objects.get(id=book_id).reviews.all()
    }
    print (Book.objects.get(id=book_id).reviews.all())
    return render(request,'book.html',context)
    
    #add Review to existing book
def add_review(request,book_id):
    user = User.objects.get(id = request.session["id"])
    book = Book.objects.get(id=book_id)
    review = Review.objects.create(review=request.POST["review"],rating=request.POST["rating"],book = book, user = user)
    book.reviews.add(review)
    user.reviewcount += 1 
    user.save()
    return redirect('/books/'+str(book_id))
#view user with information and reviews posted

def user_page(request,user_id):
    context = {
        'user' : User.objects.get(id = user_id),
        'reviews' : User.objects.get(id = user_id).reviews.all()
    }
    return render(request, 'user.html', context)