from django.urls import reverse

def menu_barbershop(request):
    """Контекстный процессор"""
    menu_context = [
        {"name": "Главная", "url": reverse("landing")},
        {"name": "О нас", "url": reverse("landing") + "#about"},
        {"name": "Преимущества", "url": reverse("landing") + "#benefits"},
        {"name": "Мастера", "url": reverse("landing") + "#masters"},
        {"name": "Услуги", "url": reverse("landing") + "#services"},
        {"name": "Запись", "url": reverse("landing") + "#booking"},
        {"name": "Спасибо", "url": reverse("thanks")},
    ]

    return menu_context