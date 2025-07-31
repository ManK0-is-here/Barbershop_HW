from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .mistral import is_bad_review

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