from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Task

@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    """Сохраняем старый статус перед изменением"""
    if instance.pk:
        old_status = Task.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
        instance._old_status = old_status
    else:
        instance._old_status = None

@receiver(post_save, sender=Task)
def send_status_change_email(sender, instance, created, **kwargs):
    """Отправляем письмо владельцу при изменении статуса"""
    if created:
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    if old_status != new_status:
        # Письмо
        subject = f"Статус задачи изменён: {instance.title}"
        text_message = (
            f"Здравствуйте, {instance.owner.username}!\n\n"
            f"Статус задачи '{instance.title}' был изменён с '{old_status}' на '{new_status}'.\n"
        )
        html_message = f"""
            <html>
                <body>
                    <p>Здравствуйте, <b>{instance.owner.username}</b>!</p>
                    <p>Статус задачи <b>'{instance.title}'</b> был изменён:</p>
                    <p>
                        <b style="color: red;">{old_status}</b> → <b style="color: green;">{new_status}</b>
                    </p>
                </body>
            </html>
        """
        recipient_list = [instance.owner.email]

        # Отправляем email
        msg = EmailMultiAlternatives(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        # Дополнительный ПРИНТ для консоли (читаемая версия)
        print("=" * 60)
        print(f"[EMAIL DEBUG - READABLE]")
        print(f"To: {', '.join(recipient_list)}")
        print(f"Subject: {subject}")
        print(f"Message:\n{text_message}")
        print("=" * 60)
