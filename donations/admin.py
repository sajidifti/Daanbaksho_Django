from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(money_donation)
admin.site.register(food_donation)
admin.site.register(cloth_donation)
admin.site.register(clothInventory)
admin.site.register(foodInventory)