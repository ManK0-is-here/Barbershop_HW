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


@login_required
def orders_list(request):

    orders = Order.objects.all().order_by('-date_created')
    return render(request,'orders_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order  = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})

def thanks(request):
    return render(request, "thanks.html")
