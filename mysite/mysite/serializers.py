from rest_framework import serializers
from .models import Car, Customer, Employee, Order, CancelOrder, RentCar, ReturnCar

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'carmodel', 'year', 'location', 'status', 'booked_by']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'age', 'address', 'phonenumber', 'active_order']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'age', 'branch']

class OrderSerializer(serializers.ModelSerializer):
     class Meta:
         model = Order
         fields = ['id', 'car_id']

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelOrder
        fields = ['id', 'car_id']

class RentCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentCar
        fields = ['id', 'car_id']

class ReturnCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnCar
        fields = ['id', 'car_id', 'car_status']