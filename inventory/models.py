import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField, FloatField, URLField, CASCADE, QuerySet
from django.utils import timezone

# Create your models here.

class Category(Document):
    name = StringField(max_length=100, required=True, unique=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'categories',
        'indexes': ['name']
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(Document):
    name = StringField(max_length=255, required=True)
    barcode = StringField(max_length=100, required=True, unique=True)
    category = ReferenceField(Category, reverse_delete_rule=CASCADE)
    description = StringField()
    price = FloatField()
    image_url = URLField()
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'products',
        'indexes': ['barcode', 'category']
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.barcode})"

class ProductScanQuerySet(QuerySet):
    def get_scans_today(self):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + datetime.timedelta(days=1)
        return self.filter(scanned_at__gte=today_start, scanned_at__lt=today_end).count()
    
    def get_scans_by_day(self, days=7):
        today = timezone.now().date()
        result = {}
        
        for i in range(days):
            date = today - datetime.timedelta(days=i)
            date_start = timezone.datetime.combine(date, timezone.datetime.min.time())
            date_end = date_start + datetime.timedelta(days=1)
            
            count = self.filter(scanned_at__gte=date_start, scanned_at__lt=date_end).count()
            result[date.strftime('%Y-%m-%d')] = count
            
        return result

class ProductScan(Document):
    product = ReferenceField(Product, reverse_delete_rule=CASCADE)
    scanned_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'product_scans',
        'indexes': ['product', 'scanned_at'],
        'queryset_class': ProductScanQuerySet
    }
    
    def __str__(self):
        return f"{self.product.name} - {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def get_scans_today(cls):
        return cls.objects.get_scans_today()
    
    @classmethod
    def get_scans_by_day(cls, days=7):
        return cls.objects.get_scans_by_day(days)
