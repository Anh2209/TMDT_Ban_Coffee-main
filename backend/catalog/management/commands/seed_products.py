from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    help = "Nap du lieu ca phe mau"

    def handle(self, *args, **options):
        samples = [
            ("Arabica Cầu Đất", "Hương hoa, chua thanh", 180000, 40, "Arabica", "light"),
            ("Robusta Buôn Ma Thuột", "Đậm, đắng mạnh", 120000, 60, "Robusta", "dark"),
            ("Blend Sáng Tạo", "Cân bằng, hậu ngọt", 150000, 25, "Arabica+Robusta", "medium"),
        ]
        for name, desc, price, stock, bean, roast in samples:
            Product.objects.get_or_create(
                name=name,
                defaults=dict(description=desc, price_vnd=price, stock=stock,
                              bean_type=bean, roast_level=roast),
            )
        self.stdout.write("Da nap xong du lieu mau")
