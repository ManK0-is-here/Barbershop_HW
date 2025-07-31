from django.contrib import admin
from .models import *
from django.db.models import Count

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    max_num = 5
    fields = ('client_name', 'rating', 'is_published')

class MastersCountFilter(admin.SimpleListFilter):
    title = "Количество мастеров"
    parameter_name = "masters_count"

    def lookups(self, request, model_admin):
        return [
            ("0", "Нет мастеров"),
            ("1-3", "От 1 до 3"),
            ("4+", "4 и более"),
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(masters_count=Count("masters"))
        if self.value() == "0":
            return queryset.filter(masters_count=0)
        if self.value() == "1-3":
            return queryset.filter(masters_count__gte=1, masters_count__lte=3)
        if self.value() == "4+":
            return queryset.filter(masters_count__gte=4)
        return queryset

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    actions = ['publish_reviews', 'unpublish_reviews'] 
    
    @admin.action(description='Опубликовать выбранные отзывы')
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
    
    @admin.action(description='Снять с публикации')
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = [MastersCountFilter] 
    actions = ['make_popular', 'make_not_popular']  
    
    @admin.action(description="Сделать популярными")
    def make_popular(self, request, queryset):
        queryset.update(is_popular=True)
    
    @admin.action(description="Сделать непопулярными")
    def make_not_popular(self, request, queryset):
        queryset.update(is_popular=False)