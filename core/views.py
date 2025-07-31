from django.shortcuts import render, redirect
from django.http import HttpResponse
from .data import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import *


def landing(request):
    masters = Master.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:6]
    return render(request, 'landing.html', {'masters': masters, 'reviews': reviews})


@login_required
def orders_list(request):
    orders = Order.objects.all().order_by('-date_created')
    
    query = request.GET.get('query', '')
    search_client_name = 'search_client_name' in request.GET
    search_phone = 'search_phone' in request.GET
    search_comment = 'search_comment' in request.GET
    
    if query:
        q_objects = Q()

        if search_client_name or not any([search_client_name, search_phone, search_comment]):
            q_objects |= Q(client_name__icontains=query)
        
        if search_phone:
            q_objects |= Q(phone__icontains=query)
        
        if search_comment:
            q_objects |= Q(comment__icontains=query)
        
        orders = orders.filter(q_objects)
    
    return render(request, 'orders_list.html', {
        'orders': orders,
        'query': query,
        'search_client_name': search_client_name,
        'search_phone': search_phone,
        'search_comment': search_comment
    })


@login_required
def order_detail(request, pk):
    order  = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})


def thanks(request):
    return render(request, "thanks.html")



def create_review(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = ReviewForm()
    
    return  render(request, 'create_review.html', {'form': form})

def create_order(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'new'
            order.save()
            form.save_m2m()
            return redirect('thanks')
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {'form': form})
