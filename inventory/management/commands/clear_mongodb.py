from django.core.management.base import BaseCommand
from inventory.models import Category, Product, ProductScan

class Command(BaseCommand):
    help = 'Clear all data from MongoDB database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MongoDB data cleanup...'))
        
        # Delete all product scans
        self.stdout.write('Deleting product scans...')
        scan_count = ProductScan.objects.count()
        ProductScan.objects.delete()
        self.stdout.write(f'  - Deleted {scan_count} product scans')
        
        # Delete all products
        self.stdout.write('Deleting products...')
        product_count = Product.objects.count()
        Product.objects.delete()
        self.stdout.write(f'  - Deleted {product_count} products')
        
        # Delete all categories except Uncategorized
        self.stdout.write('Deleting categories...')
        category_count = Category.objects.count()
        
        # Keep or recreate Uncategorized category
        try:
            uncategorized = Category.objects.get(name="Uncategorized")
            # Delete all categories
            Category.objects.delete()
            # Recreate Uncategorized
            uncategorized = Category(name="Uncategorized")
            uncategorized.save()
            self.stdout.write(f'  - Deleted {category_count-1} categories (kept Uncategorized)')
        except:
            # Delete all categories
            Category.objects.delete()
            # Create Uncategorized
            uncategorized = Category(name="Uncategorized")
            uncategorized.save()
            self.stdout.write(f'  - Deleted {category_count} categories and created Uncategorized')
        
        self.stdout.write(self.style.SUCCESS('MongoDB data cleanup completed successfully!')) 