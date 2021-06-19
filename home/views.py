from base64 import b64encode
from django.shortcuts import render, redirect,reverse
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
import hashlib
import telebot
import time
from .forms import *
import requests


bot = telebot.TeleBot('1756376023:AAFNHBzVvdcx2rh1f_Xsc8lKbz0-pzFFqP0')
ids = ['344548620', '412228067']


def myajaxtestview(request):
    device = request.COOKIES['device']
    order_id=request.POST['order_id']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderdict={}
    orderdict['phone'] = request.POST['phone']
    orderdict['name'] = request.POST['name']
    orderdict['adress'] = request.POST['adress']
    ord_type='card'
    send_info(order, orderdict,ord_type,order_id)
    order.delete()

def send_info(order,orderdict,ord_rype,ord_id=None):
    for id in ids:
        order_str=''
        items=list(order.orderitem_set.all())
        print(items)
        for item in items:
            order_str+=f'Продукт:{item.product.name}\nКоличество:{item.quantity}\nОписание:{item.product.description}\n_____________________\n'
        for key in orderdict.keys():
            order_str+='\n'+key+': '+orderdict[key]
        if ord_rype=='card':
            order_str+=f'\nЗаказ картой\nНомер заказа:{ord_id}'
        else:
            order_str+='\n ну бля обычный заказ нахуй тебе айди)'
        bot.send_message(id, order_str)
        time.sleep(1)

def send_form(mess_dict):
    message=''
    if 'date' in mess_dict:
        message+='Нам поступил заказ столика:\n'+'Имя:'+mess_dict['name']+'\nСообщение:'+mess_dict['message']+\
                '\nТелефон:'+mess_dict['phone']\
                +'\nДата:'+mess_dict['date']\
                +'\nВремя:'+mess_dict['time']\
                +'\nКоличество человек:'+mess_dict['people']
    else:
        message+='Нам поступило сообщение:\n'+'Имя:'+mess_dict['name']+'\nСообщение:'+mess_dict['message']+\
                '\nТелефон:'+mess_dict['phone']\
                +'\nПочта: '+mess_dict['email']
    for id in ids:
        bot.send_message(id,message)


def store(request):
    if request.method == 'POST':
        mess_dict={}
        mess_dict['name']=request.POST['name']
        mess_dict['message']=request.POST['message']
        mess_dict['phone']=request.POST['phone']
        try:
            mess_dict['date']=request.POST['date']
            mess_dict['time']=request.POST['time']
            mess_dict['people']=request.POST['people']
        except:
            mess_dict['email']=request.POST['email']
        send_form(mess_dict)
    products = Product.objects.all()
    categories= Category.objects.all()
    context = {'products' : products, "categories":categories
    }

    return render(request, 'home/index.html', context)

def delivery(request):
    return render(request,'home/delivery.html')


def privacy_policy(request):
    return render(request,'home/privacypolicy.html')


def cart(request):
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order_id=device+str(time.time())
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    amount=order.get_cart_total
    checkout={'public_key':'i67910001878',
              'private_key':'b8sDbUFGnZMTGXV5gy7z1tb687cqn5CqBsFoDw4f',
              'version':3,
              'action':'pay',
              'amount':amount,
              'currency':'UAH',
              'description':'test',
              'order_id':order_id,
              'result_url':'https://vk.com/morgenshtern?z=audio_playlist-2000618831_11618831%2F77ef1d65a8a66736ff'
              }
    enc_checkout=b64encode(json.dumps(checkout).encode("utf-8")).decode("ascii")
    sign_string=checkout['private_key']+enc_checkout+checkout['private_key']
    sign_enc = b64encode(hashlib.sha1(sign_string.encode('ascii')).digest()).decode("ascii")

    CHOICES = [('M', 'Оплата наличными при получении'), ('F', 'Оплата картой')]
    Gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
    context = {'order':order,'checkout_data':enc_checkout,'signature':sign_enc,'form':Gender,'order_id':order_id}
    if request.method == 'POST':
        orderdict={}
        orderdict['name']=request.POST['name']
        orderdict['adress']=request.POST['adress']
        orderdict['phone']=request.POST['phone']
        ord_type='cash'
        send_info(order,orderdict,ord_type,order_id)
        order.delete()
        opt=request.POST['option']
        return render(request,'home/index.html')
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
