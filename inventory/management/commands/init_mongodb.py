from django.core.management.base import BaseCommand
from inventory.models import Category, Product, ProductScan
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Initialize MongoDB database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MongoDB initialization...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Category.objects.delete()
        Product.objects.delete()
        ProductScan.objects.delete()
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = [
            Category(name="Electronics"),
            Category(name="Food"),
            Category(name="Clothing"),
            Category(name="Books"),
            Category(name="Toys"),
            Category(name="Uncategorized")
        ]
        
        for category in categories:
            category.save()
            self.stdout.write(f'  - Created category: {category.name}')
        
        # Create sample products
        self.stdout.write('Creating sample products...')
        products = [
            {
                'name': 'Smartphone X',
                'barcode': '1234567890123',
                'category': categories[0],  # Electronics
                'description': 'Latest smartphone with amazing features',
                'price': 999.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Chocolate Bar',
                'barcode': '2234567890123',
                'category': categories[1],  # Food
                'description': 'Delicious milk chocolate',
                'price': 2.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'T-Shirt',
                'barcode': '3234567890123',
                'category': categories[2],  # Clothing
                'description': 'Cotton t-shirt, size L',
                'price': 19.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Python Programming',
                'barcode': '4234567890123',
                'category': categories[3],  # Books
                'description': 'Learn Python programming from scratch',
                'price': 34.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Action Figure',
                'barcode': '5234567890123',
                'category': categories[4],  # Toys
                'description': 'Collectible action figure',
                'price': 24.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Wireless Headphones',
                'barcode': '6234567890123',
                'category': categories[0],  # Electronics
                'description': 'Noise-cancelling wireless headphones',
                'price': 149.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Cereal Box',
                'barcode': '7234567890123',
                'category': categories[1],  # Food
                'description': 'Breakfast cereal with whole grains',
                'price': 4.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Jeans',
                'barcode': '8234567890123',
                'category': categories[2],  # Clothing
                'description': 'Blue denim jeans, size 32',
                'price': 49.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Mystery Novel',
                'barcode': '9234567890123',
                'category': categories[3],  # Books
                'description': 'Bestselling mystery novel',
                'price': 14.99,
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'name': 'Board Game',
                'barcode': '0234567890123',
                'category': categories[4],  # Toys
                'description': 'Family board game for 2-6 players',
                'price': 29.99,
                'image_url': 'https://via.placeholder.com/150'
            }
        ]
        
        created_products = []
        for product_data in products:
            product = Product(**product_data)
            product.save()
            created_products.append(product)
            self.stdout.write(f'  - Created product: {product.name}')
        
        # Create sample scans
        self.stdout.write('Creating sample product scans...')
        # Create some scans for today and past days
        for i in range(30):
            # Random product
            product = random.choice(created_products)
            # Random date in the last 7 days
            days_ago = random.randint(0, 7)
            scan_date = timezone.now() - timezone.timedelta(days=days_ago)
            
            scan = ProductScan(
                product=product,
                scanned_at=scan_date
            )
            scan.save()
            
        self.stdout.write(f'  - Created {30} sample scans')
        
        self.stdout.write(self.style.SUCCESS('MongoDB initialization completed successfully!')) 