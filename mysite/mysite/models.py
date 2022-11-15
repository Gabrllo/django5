from django.db import models

# Car db model
class Car(models.Model):
    make = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    year = models.CharField(max_length=35)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    booked_by = models.CharField(max_length=50)

    def __str__(self):
        return self.make + ' ' + self.carmodel

# Customer db model
class Customer(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    active_order = models.BooleanField()

    def __str__(self):
        return self.name

# Employee db model
class Employee(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    car_id = models.CharField(max_length=50)

    def __str__(self):
        return self.car_id

class CancelOrder(models.Model):
    car_id = models.CharField(max_length=50)

    def __str__(self):
        return self.car_id

class RentCar(models.Model):
    car_id = models.CharField(max_length=50)

    def __str__(self):
        return self.car_id

class ReturnCar(models.Model):
    car_id = models.CharField(max_length=50)
    car_status = models.CharField(max_length=50)

    def __str__(self):
        return self.car_id