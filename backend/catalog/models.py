from django.db import models


class Product(models.Model):
    ROAST_CHOICES = [
        ("light", "Rang nhạt"),
        ("medium", "Rang vừa"),
        ("dark", "Rang đậm"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_vnd = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    bean_type = models.CharField(max_length=50)
    roast_level = models.CharField(max_length=10, choices=ROAST_CHOICES)
    weight_g = models.PositiveIntegerField(default=500)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
