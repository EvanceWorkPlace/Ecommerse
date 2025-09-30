from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, PasswordForm,UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.filter(user__id=request.user.id).first()
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            profile = form.save(commit=False)
            if not current_user:
                profile.user = request.user
            profile.save()
            messages.success(request,'User Info has been Updated!!!')
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.success(request, "You must be logged In to Access That Page")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            password_form = PasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Your Password has been updated. Please login.")
                login(request, request.user)
                return redirect('home')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            password_form = PasswordForm(request.user)
        return render(request, "update_password.html", {'password_form': password_form})
    else:
        messages.success(request,'You must be logged in..')
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request,'User has been Updated!!!')
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You must be logged In to Access That Page")
        return redirect('home')

    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        

        if user is not None:
            login(request, user)
            # do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #get the saved card from database
            saved_cart = current_user.old_cart
            #Convert database string to python dictionary
            if saved_cart:
                #convert using json
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictory to our session
                # get the cart
                cart = Cart(request)
                #Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, ("You have been Log In..."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, Try again!"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been Logged out.."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("You have register successfully Welcomee.."))
            return redirect('update_user')
        else:
            messages.success(request, ("Something went wrong! Try again.."))
            return redirect('register')
    else:
        return render(request, 'register.html' , {'form':form})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request,foo):
    foo = foo.replace('-', '')

    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products , 'category':category})
    except:
        messages.success(request, ("Something went wrong! Try again.."))
        return redirect('home')

def search(request):
    # determine if they filled out the form
    if request.method == "POST":
        searched_value = request.POST.get('searched', '')
        # query of products in The db model
        searched = Product.objects.filter(Q(name__icontains=searched_value) | Q(description__icontains=searched_value))
        # Test for null
        if not searched:
            messages.success(request,'Sorry that Product does not exist..Please try again')
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})
