from .models import Car, Customer, Employee
from rest_framework.response import Response
from .serializers import CarSerializer, CustomerSerializer, EmployeeSerializer, OrderSerializer
from .serializers import RentCarSerializer, CancelOrderSerializer, ReturnCarSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view


# Cars
@api_view(['GET'])
def get_cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    print(serializer.data)
    print('serializer.data id: ')
    print(serializer.data[0]['id'])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_car(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(theCar, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    theCar.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Orders
@api_view(["PUT"])
def order_car(request, id):
    try:
        theCustomer=Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if theCustomer.active_order == True:
        return Response("Customer has a booking registered", status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        try:
            theCar = Car.objects.get(pk=serializer.data['car_id'])
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if theCar.status == "booked":
            return Response("Car is already booked", status=status.HTTP_403_FORBIDDEN)
        else:
            Car.objects.filter(pk=serializer.data['car_id']).update(status="booked")
            Car.objects.filter(pk=serializer.data['car_id']).update(booked_by=id)

        Customer.objects.filter(pk=id).update(active_order=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def cancel_order(request, id):
    try:
        theCustomer=Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if theCustomer.active_order == False:
        return Response("Customer has no booking registered", status=status.HTTP_403_FORBIDDEN)

    serializer = CancelOrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        try:
            theCar = Car.objects.get(pk=serializer.data['car_id'])
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if theCar.status == "booked" and theCar.booked_by == str(id):
            Car.objects.filter(pk=serializer.data['car_id']).update(status='available')
            Car.objects.filter(pk=serializer.data['car_id']).update(booked_by="None")
        else:
            return Response("This car is booked by someone else, or is not booked by you", status=status.HTTP_403_FORBIDDEN)

        Customer.objects.filter(pk=id).update(active_order=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def rent_car(request, id):
    try:
        theCustomer=Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if theCustomer.active_order == False:
        return Response("Customer has no booking registered", status=status.HTTP_403_FORBIDDEN)

    serializer = RentCarSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        try:
            theCar = Car.objects.get(pk=serializer.data['car_id'])
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if theCar.status == "booked" and theCar.booked_by == str(id):
            Car.objects.filter(pk=serializer.data['car_id']).update(status='rented')
        else:
            return Response("This car is booked by someone else, or is not booked by you", status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def return_car(request, id):
    try:
        theCustomer=Customer.obje2cts.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if theCustomer.active_order == False:
        return Response("Customer has no booking registered, must be a trick", status=status.HTTP_403_FORBIDDEN)

    serializer = ReturnCarSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        try:
            theCar = Car.objects.get(pk=serializer.data['car_id'])
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if theCar.booked_by != str(id):
            return Response("This car was not booked by you", status=status.HTTP_403_FORBIDDEN)
        elif serializer.data['car_status'] == 'ok':
            Car.objects.filter(pk=serializer.data['car_id']).update(status='available')
            Car.objects.filter(pk=serializer.data['car_id']).update(booked_by="None")
            Customer.objects.filter(pk=id).update(active_order=False)
        else:
            Car.objects.filter(pk=serializer.data['car_id']).update(status='damaged')
            Car.objects.filter(pk=serializer.data['car_id']).update(booked_by="None")
            Customer.objects.filter(pk=id).update(active_order=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Customers
@api_view(["GET"])
def get_customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def save_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_customer(request, id):
    try:
        the_customer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(the_customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_customer(request, id):
    try:
        the_customer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    the_customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Employees
@api_view(['GET'])
def get_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def save_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_employee(request, id):
    try:
        the_employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EmployeeSerializer(the_employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_employee(request, id):
    try:
        the_employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    the_employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)