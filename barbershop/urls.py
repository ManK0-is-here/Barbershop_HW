from django.contrib import admin
from core.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('users/', include('users.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

