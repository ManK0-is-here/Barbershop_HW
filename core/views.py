from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *


def landing(request):
    context = {
        "title": "Барбершоп: напоят и побьют",
        "masters": masters[:4],
        "services": services,
    }
    return render(request, "landing.html", context)


def orders_list(request):
    context = {
        "orders": orders,
        "title": "Список заявок",
    }
    return render(request, "orders_list.html", context)

def order_detail(request):
    context = {
        "order": orders,
        "title": "Заявка",
    }
    return render(request, "order_detail.html", context)

def base(request):
    return landing(request)

def thanks(request):
    return render(request, "thanks.html")
