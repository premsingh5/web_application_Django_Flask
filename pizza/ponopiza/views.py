from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import items,toppings,category,placedorders,placedtoppings
import copy
# Create your views here.
placed_orders=[]
incartlist=[]
def index(request):
    if not request.user.is_authenticated:
        return(render(request,"users/login.html",{"message":None}))
    context = {
    "user":request.user,
    "items":items.objects.all(),
    "groups":category.objects.all(),
    "toppigs":toppings.objects.all()
    }
    return(render(request,"users/index.html",context))
def userpage(request):
    context={
    "user":request.user
    }
    return(render(request,"users/userpage.html",context))


def loadregister(request):
    return(render(request,"users/register.html"))
def register(request):
    try:
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
    except KeyError:
        return(render(request,"users/error.html",{"message":"No Selection"}))
    user=User.objects.create_user(username,email,password)
    user.first_name=first_name
    user.last_name=last_name
    user.save()
    return(render(request,"users/login.html",{"message":"Succesfully Registered"}))
def login_view(request):
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return(HttpResponseRedirect(reverse("index")))
    else:
        return(render(request,"users/login.html",{"message":"Invalid credentials"}))
def logout_view(request):
    logout(request)
    return(render(request,"users/login.html",{"message":"Logged out Succesfully"}))
def confirmation(request):
    total_amount=0
    if len(incartlist)>=1:
        for item in incartlist:
            total_amount += item["price"]
    context={
    "total_amount":total_amount,
    "incartlist":incartlist
    }
    return(render(request,"users/confirmation.html",context))
def menu(request,category_name):
    try:
        catg=category.objects.get(name=category_name)
    except category.DoesNotExist:
        raise Http404("category doesnot exist")
    list=catg.itemslist.all()
    is_pizza=False
    if category_name=="pizza":
        is_pizza=True

    context={
    "itemlist":list,
    "category":catg,
    "groups":category.objects.all(),
    "category_name":category_name,
    "toppings":toppings.objects.all(),
    "is_pizza":is_pizza
    }

    return(render(request,"users/mainpage1.html",context))

def addtocart(request,item_name):
    size=request.POST["size"]
    selectedtoppings=request.POST.getlist('selectedtoppings')
    noftpg=len(selectedtoppings)
    if noftpg>3:
        noftpg=5
    item=items.objects.get(itemsname=item_name,topngNO=noftpg)
    if size=="large":
        Price=item.large
    else:
        Price=item.small
    a={"itemsname":item_name,"det":item,"size":size,"price":Price,"selectedtoppings":selectedtoppings}
    incartlist.append(a)

    context={
    "incart":incartlist,
    "number":len(incartlist)
    }
    return(render(request,"users/orders1.html",context))
def cartpage(request):
    len(incartlist)
    context={
    "incart":incartlist,
    "number":len(incartlist)
    }
    return(render(request,"users/orders1.html",context))


def myorders(request):
    context={
    "placed_orders":placed_orders
    }
    return(render(request,"users/myorders.html",context))

def placeorder(request):
    user=request.user
    arr=copy.deepcopy(incartlist)
    for item in arr:
        s=placedorders(orderuser=user,ordername=item["itemsname"],price=item["price"],size=item["size"])
        s.save()
        for topping in item["selectedtoppings"]:
            T=placedtoppings(ordertoppingname=topping)
            T.save()
            T.order.add(s)
        placed_orders.append(item)
    incartlist.clear()
    return(HttpResponseRedirect(reverse("index")))
def Allorders(request):
    user=request.user
    superusers=User.objects.filter(is_superuser=True)
    if user in superusers:
        context={
        "placedorders":placedorders.objects.all(),
        "placedtoppings":placedtoppings.objects.all()
        }
        return(render(request,"users/Allorders.html",context))
    else:
        return(render(request,"users/error.html",{"message":"Forbidden"}))
