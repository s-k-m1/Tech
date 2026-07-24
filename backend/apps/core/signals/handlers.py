from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.models import User, AuditLog


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            tenant=instance.tenant,
            user=instance,
            action="user_created",
            resource="user",
            details={"user_type": instance.user_type},
        )
