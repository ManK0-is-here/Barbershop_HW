from django.db import models

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")

    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография", null=True)

    phone = models.CharField(max_length=20, verbose_name="Телефон")

    address = models.CharField(max_length=256, verbose_name="Адрес")

    experience = models.PositiveIntegerField(
        verbose_name="Стаж работы",
        help_text="Опыт работы в годах")

    services = models.ManyToManyField(
        "Service",
        related_name="masters",
        verbose_name="Услуги")

    is_active = models.BooleanField(
        default=True, 
        verbose_name="Активен")
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural="Мастера"


class Order(models.Model):
    STATUS_CHOICES = [
        ('not_approved', 'Не подтверждена'),
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('cancelled', 'Отменена'),
        ('completed', 'Выполнена')
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")

    phone = models.CharField(max_length=20, verbose_name="Телефон")

    comment = models.TextField(blank=True, verbose_name="Комментарий")

    status = models.CharField (
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="not_approved", 
        verbose_name="Статус")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания") 

    date_updated = models.DateTimeField(null=True, auto_now=True, verbose_name="Дата обновления")

    master = models.ForeignKey(
        "Master",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мастер")
    
    services = models.ManyToManyField(
        "Service",
        related_name="orders",
        verbose_name="Услуги"
    )
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ #{self.id}: {self.client_name}"
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural="Записи"


class Service(models.Model):

    name = models.CharField(max_length=200, verbose_name="Название")

    description = models.TextField(blank=True, verbose_name="Описание")

    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена")
    
    duration = models.PositiveIntegerField (verbose_name="Длительность", help_text="Время выполнения в минутах")

    is_popular = models.BooleanField(default=False,  verbose_name="Популярная услуга")

    image = models.ImageField(
        null=True,
        upload_to="services/", 
        blank=True,
        verbose_name="Изображение")

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural="Услуги"


class Review(models.Model):

    AI_STATUS_CHOICES = [
        ('ai_checked_true', '✅ Проверено ИИ'),
        ('ai_cancelled', '❌ Отклонено ИИ'),
        ('in_progress', '🔄 В процессе'),
        ('not_checked', '⏳ Не проверено'),
    ]
    
    ai_status = models.CharField(
        max_length=20,
        choices=AI_STATUS_CHOICES,
        default='not_checked',
        verbose_name='Статус модерации'
    )

    RATING_CHOICES = [
        (1, "Ужасно, плохо, нехорошо"),
        (2, "Плохо но хотябы жив"),
        (3, "Нормально нормально"),
        (4, "Хорошо"),
        (5, "Супер ультра мега хорошо")
    ]
    
    text = models.TextField(verbose_name="Текст отзыва")

    client_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Имя клиента")
    
    master = models.ForeignKey(
        "Master",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Мастер")
    
    photo = models.ImageField(
        upload_to="reviews/", 
        blank=True, 
        null=True,
        verbose_name="Фотография")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name="Оценка")
    
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    def __str__(self):
        return f"Отзыв #{self.id} - {self.get_rating_display()}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural="Отзывы"