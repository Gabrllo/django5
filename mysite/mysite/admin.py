from django.contrib import admin
from .models import Car, Customer, Employee, Order, CancelOrder, RentCar, ReturnCar

admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(CancelOrder)
admin.site.register(RentCar)
admin.site.register(ReturnCar)
