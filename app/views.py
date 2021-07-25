from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        user = User.objects.filter(email = request.POST['email'])
        request.session['userid'] = user[0].id
        request.session['name'] = user[0].first_name

        context = {
            'all_items': Item.objects.all()
        }
        return render(request, 'main.html',context)
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        user = User.objects.filter(email = request.POST['email'])
        request.session['userid'] = user[0].id
        request.session['name'] = user[0].first_name
        context = {
            'user': User.objects.get(id=request.session['userid']),
            'all_items': Item.objects.all()
        }
        return render(request, 'main.html',context)
    return redirect('/')

def add_item(request):
    if request.method == "POST":
        errors = Item.objects.item_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/add_item')
        user = User.objects.get(id=request.session["userid"])
        item = Item.objects.create(
            item = request.POST['item'],
            description = request.POST['description'],
            price = request.POST['price'],
            uploaded_by = user
        )
        return redirect('/all_items')
    return render(request, 'add_item.html')

def all_items(request):
    if "userid" not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid']),
            'all_items': Item.objects.all()
        }
    return render(request, 'main.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def user(request,user_id):
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'edit_account.html',context)

def user_edit(request,user_id):
    if "userid" not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = User.objects.validate_edit(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f'/user/{user_id}')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user = User.objects.get(id=user_id)
        user.password = pw_hash
        user.save()
        user.email = request.POST['email']
        user.save()
        return redirect('/all_items')
    return redirect('/')


def item(request, item_id):
    context ={
        'item': Item.objects.get(id=item_id)
    }
    return render(request, 'item.html', context)

def edit(request,item_id):
    context ={
        'item': Item.objects.get(id=item_id)
    }
    return render(request, 'edit_item.html',context)

def make_edit(request, item_id):
    if "userid" not in request.session:
        return redirect('/')
    errors = Item.objects.item_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
             messages.error(request,value)
        return redirect(f'/item/{item_id}/edit')
    item = Item.objects.get(id=item_id)
    item.item = request.POST['item']
    item.save()
    item.description = request.POST['description']
    item.save()
    item.price = request.POST['price']
    item.save()
    return redirect('/all_items')

def add_cart(request,item_id):
    item = Item.objects.get(id=item_id)
    OrderItem.objects.create(
        item = item
    )
    return redirect('/all_items')

def view_cart(request):
    context ={
        'items' : OrderItem.objects.all()
    }
    return render(request, 'cart.html',context)

def remove(request,item_id):
    c = OrderItem.objects.get(id=item_id)
    c.delete()
    return redirect('/view_cart')
    
    
def delete_item(request, item_id):
    c = Item.objects.get(id=item_id)
    c.delete()
    return redirect('/all_items')

