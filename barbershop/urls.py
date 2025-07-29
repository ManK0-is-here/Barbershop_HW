from django.contrib import admin
from django.urls import path
from core.views import(
    landing,
    orders_list,
    thanks,
    order_detail,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("index/", index, name="index"),
    # path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('order/<int:order_id>/', order_detail, name='order_detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
