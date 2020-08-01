from django.contrib import admin
from .models import category,items,toppings,placedorders,placedtoppings

admin.site.register(category)
admin.site.register(items)
admin.site.register(toppings)
admin.site.register(placedorders)
admin.site.register(placedtoppings)
