from django.db.models import Q
from .forms import *
from .models import *
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(
            is_published=True
        ).order_by('-created_at')[:6]

        return context


class OrdersListView(LoginRequiredMixin, ListView):

    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):

        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        
        if query:
            q_objects = Q()

            if 'search_client_name' in self.request.GET or not any([
                'search_client_name',
                'search_phone',
                'search_comment'
            ]):
                q_objects |= Q(client_name__icontains=query)
            
            if 'search_phone' in self.request.GET:
                q_objects |= Q(phone__icontains=query)
            
            if 'search_comment' in self.request.GET:
                q_objects |= Q(comment__icontains=query)
            
            queryset = queryset.filter(q_objects)
        
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['search_client_name'] = 'search_client_name' in self.request.GET
        context['search_phone'] = 'search_phone' in self.request.GET
        context['search_comment'] = 'search_comment' in self.request.GET

        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'


class ThanksView(TemplateView):
    template_name = 'thanks.html'



class ReviewCreateView(CreateView):

    model = Review
    form_class = ReviewForm
    template_name = 'create_review.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(
            self.request,
            'Отзыв отправлен! Спасибо что настолько смелые!'
        )
        
        return response

class OrderCreateView(CreateView):

    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
    
        order = form.save(commit=False)
        order.status = 'new'
        order.save()
        form.save_m2m()
        
        messages.success(
            self.request,
            'Заявка создана! Скоро с вами обязательно наверно вяжутся для подтверждения.'
        )
        
        return super().form_valid(form)
