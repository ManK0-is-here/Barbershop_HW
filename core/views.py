from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



def landing(request):
    masters = Master.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:6]
    return render(request, 'landing.html', {'masters': masters, 'reviews': reviews})


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

def thanks(request):
    return render(request, "thanks.html")
