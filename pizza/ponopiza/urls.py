from django.urls import path
from . import views
urlpatterns =[
    path("",views.index,name="index"),
    path("userpage",views.userpage,name="userpage"),
    path("cartpage",views.cartpage,name="cartpage"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("loadregister",views.loadregister,name="loadregister"),
    path("placeorder",views.placeorder,name="placeorder"),
    path("confirmation",views.confirmation,name="confirmation"),
    path("myorders",views.myorders,name="myorders"),
    path("allorders",views.Allorders,name="allorders"),
    path("<str:category_name>",views.menu,name="menu"),
    path("<path:item_name>/addtocart",views.addtocart,name="addtocart"),
    #path("menu/cartview",views.cart_view,name="cart_view"),
    #path("menu/remove",views.remove,name="remove"),
    #path("menu/placedorder",views.placeorder,name="placedorders")


]
