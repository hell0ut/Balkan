from base64 import b64encode,b64decode
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django import forms
import json
import hashlib
import telebot
import time


def send_info(order):
    bot = telebot.TeleBot('1756376023:AAFNHBzVvdcx2rh1f_Xsc8lKbz0-pzFFqP0')
    ids=['344548620','412228067']
    for id in ids:
        order_str=''
        items=list(order.orderitem_set.all())
        print(items)
        for item in items:
            order_str+=f'Продукт:{item.product.name}\nКоличество:{item.quantity}\nОписание:{item.product.description}\n_____________________\n'
        order_str+=f'адрес\nжопа\nалан гей'
        bot.send_message(id, order_str)
        time.sleep(1)

def store(request):
    products = Product.objects.all()
    categories= Category.objects.all()

   # device = request.COOKIES['device']
   # customer, created = Customer.objects.get_or_create(device=device)
   # order, created = Order.objects.get_or_create(customer=customer, complete=False)
   # cartItems=order.get_cart_items

    context = {'products' : products, "categories":categories#,'cartItems':cartItems
    }

    return render(request, 'home/index.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        #Get user account information
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity=request.POST['quantity']
        orderItem.save()

        return redirect('cart')

    context = {'product':product}
    return render(request, 'home/product.html', context)


def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    amount=order.get_cart_total
    checkout={'public_key':'sandbox_i10524492600',
              'private_key':'sandbox_cbF2ohPDgJoi3fiUrxEJjqh6BHVqzKaZKXIOX0xK',
              'version':3,
              'action':'pay',
              'amount':amount,
              'currency':'UAH',
              'description':'test',
              'order_id':'02345982345'
              }
    enc_checkout=b64encode(json.dumps(checkout).encode("utf-8")).decode("ascii")
    sign_string=checkout['private_key']+enc_checkout+checkout['private_key']
    sign_enc = b64encode(hashlib.sha1(sign_string.encode('ascii')).digest()).decode("ascii")
    print(sign_enc)

    CHOICES = [('M', 'Оплата наличными при получении'), ('F', 'Оплата картой')]
    Gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
    context = {'order':order,'checkout_data':enc_checkout,'signature':sign_enc,'form':Gender}
    if request.method == 'POST':
        send_info(order)
        return redirect('store')
    return render(request, 'home/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    if action=='delete':
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)
