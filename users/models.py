from django.db import models
import uuid

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.BigIntegerField(unique=True)
    pocket_id = models.BigIntegerField(null=True, blank=True, unique=True)
    is_registered = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    progress = models.IntegerField(default=0)
    current_lesson = models.IntegerField(default=0)
    user_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    click_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"User {self.telegram_id} - Registered: {self.is_registered}"
    
    def generate_click_id(self, length=10):
        import random
        import string
        self.click_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        self.save()

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
    