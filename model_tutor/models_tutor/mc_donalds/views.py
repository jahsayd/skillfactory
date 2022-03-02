from django.shortcuts import render

# Create your views here.

fries_stand = Product(name='Картофель фри (станд.)', price=93.0)
fries_stand.save()

fries_big = Product.objects.create(name='Картофель фри (бол.)', price=106.0)

 from rest.models import Order
Order.objects.create(staff = cashier1, take_away = False)
Order.objects.create(staff = cashier2, take_away = True)
Order.objects.create(staff = cashier1, take_away = True)