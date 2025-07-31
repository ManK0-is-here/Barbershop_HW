from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .mistral import is_bad_review
from django.db.models.signals import m2m_changed
from .telegram import send_telegram_message

@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    if created:
        # Меняем статус на "В процессе проверки"
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save(update_fields=['ai_checked_status'])
        
        # Вызываем функцию модерации
        try:
            if is_bad_review(instance.text):
                instance.ai_checked_status = "ai_cancelled"
                instance.is_published = False
            else:
                instance.ai_checked_status = "ai_checked_true"
                instance.is_published = True
                
            instance.save(update_fields=['ai_checked_status', 'is_published'])
        except Exception:
            instance.ai_checked_status = "ai_checked_false"
            instance.save(update_fields=['ai_checked_status'])


@receiver(m2m_changed, sender=Order.services.through)
def notify_new_order(sender, instance, action, **kwargs):

    if action == "post_add":
        services = "\n".join([f"- {service.name}" for service in instance.services.all()])
        
        message = (
            f"*Новый заказ!* 🎉\n"
            f"*Клиент:* {instance.client_name}\n"
            f"*Телефон:* `{instance.phone}`\n"
            f"*Мастер:* {instance.master.name if instance.master else 'Не назначен'}\n"
            f"*Дата:* {instance.appointment_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"*Услуги:*\n{services}"
        )
        
        send_telegram_message(message)            