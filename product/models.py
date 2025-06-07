from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    price = models.IntegerField(default=0)
    size = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            import random
            import string

            from django.utils import timezone

            today = timezone.now().strftime("%Y%m%d")
            random_part = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=5)
            )
            self.sku = f"SP-{today}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.size})"
