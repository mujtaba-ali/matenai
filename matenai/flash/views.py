from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser


from .models import Restaurant, User, Menu

# Create your views here.
def index(request):
    print(request.user == AnonymousUser())
    if request.user != AnonymousUser():
        if request.user.is_res:
            restaurant = Restaurant.objects.filter(res_id=request.user.id)
            if not restaurant:
                return render(request, 'res_register.html', {'res_reg': 'no menu'})
            return render(request, 'res_index.html')
        return render(request, 'index.html')
    return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(request.user.is_res)
            if request.user.is_res:
                restaurant = Restaurant.objects.filter(res_id=request.user.id)
                if restaurant:
                    return HttpResponseRedirect(reverse("index"))
                return render(request, 'res_register.html', {'res_reg': 'no menu'})
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'login.html', {'message': 'Incorrect Username or Password'})
    
    if request.user == AnonymousUser():
        return render(request, "login.html")
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        is_restaurant = eval(request.POST["is_res"])

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not password or not confirmation or not email:
            return render(request, 'register.html', {'message': 'All fields must be filled!'})

        if password != confirmation:
            return render(request, 'register.html', {'message': 'Passwords must match!'})

        try:
            user = User.objects.create_user(username = username, email = email, password = password, is_res = is_restaurant)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {'message': 'Username already taken!'})
        
        login(request, user)
        if request.user.is_res:
            return render(request, 'res_register.html', {'is_res': 'no menu'})
        return HttpResponseRedirect(reverse('index'))

    if request.user == AnonymousUser():
        return render(request, 'register.html')
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def res_register(request):
    if request.user.is_res:
        if request.method == 'POST':
            res_id = int(request.user.id)
            res_name = request.POST["res_name"]
            image_url = request.POST["image_url"]
            cuisine = request.POST["cuisine"]
            address = request.POST["address"]
            zip_code = request.POST["zip_code"]

            # zipcode verification

            try:
                res = Restaurant.objects.create(res_id_id=res_id, res_name=res_name.lower(), 
                image_url=image_url, cuisine=cuisine, address=address, zip_code=zip_code)

                res.save()
            except IntegrityError:
                return render(request, 'res_register.html', {'message': 'A Restaurant with the name already exists!'})
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'res_register.html')
    return HttpResponseRedirect(reverse('index'))

def res_index(request, res_name):
    # if restaurant, display current orders and if menu not added, redirect to add menu 
    if request.user.is_res:
        restaurant = Restaurant.objects.get(res_name=res_name)

        if restaurant:
            return render(request, 'res_index.html')
        return render(request, 'res_register.html', {'message': 'Restaurant does not exist. Create new here'})
    # if customer, display restaurant details and menu
    else:
        return render(request, 'res_info.html')

    
def add_menu(request):
    if request.user == AnonymousUser():
        return HttpResponseRedirect('/')
    if request.user.is_res:
        menu = Menu.objects.filter(res_id_id=request.user.id)
        if not menu:
            if request.method == 'POST':
                menu_items = request.POST.getlist("item")
                prices = request.POST.getlist("price")
                if '' in menu_items or '' in prices:
                    return render(request, 'add_menu.html', {'message': 'All fields must be filled! Remove extra fields if any.'})
                
                for item, price in zip(menu_items, prices):
                    try:
                        menu = Menu.objects.create(res_id_id=int(request.user.id), item = item, price = price)
                        menu.save()
                    except IntegrityError:
                        return render(request, 'add_menu.html', {'message': 'One or more of the items already exist'})
                return HttpResponseRedirect('/')
            return render(request, 'add_menu.html', {'res_reg':'no_menu'})
        return HttpResponseRedirect('/edit_menu')
    return HttpResponseRedirect('/')


def menu(request):
    if request.user == AnonymousUser():
        return HttpResponseRedirect('/')

    if request.user.is_res:
        menu = Menu.objects.filter(res_id_id=request.user.id)
        if menu:
            return render(request, 'menu.html', {'menu': menu})
        return render(request, 'menu.html')
    return HttpResponseRedirect('/')

def edit_menu(request):
    if request.user == AnonymousUser():
        return HttpResponseRedirect('/')

    if request.user.is_res:
        menu = Menu.objects.filter(res_id_id=request.user.id)
        if menu:
            return render(request, 'edit_menu.html', {'menu': menu})
        return render(request, 'menu.html')
    return HttpResponseRedirect('/')