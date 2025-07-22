from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
import concurrent.futures
import time
from .models import Category, Product, ProductScan
from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from bson import ObjectId, errors as bson_errors
from django.contrib.auth.decorators import login_required

def index(request):
    """Home page view"""
    return render(request, 'inventory/index.html')

@login_required
def dashboard(request):
    """Dashboard view with analytics"""
    # Get product and category counts
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    
    # Get products by category for chart
    categories = []
    for category in Category.objects.all():
        product_count = Product.objects(category=category).count()
        categories.append({
            'id': str(category.id),
            'name': category.name,
            'product_count': product_count
        })
    
    # Sort categories by product count
    categories = sorted(categories, key=lambda x: x['product_count'], reverse=True)
    
    # Get recent products
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    # Get today's scan count
    scans_today = ProductScan.get_scans_today()
    
    # Get scan history for the last 7 days
    scan_history = ProductScan.get_scans_by_day(7)
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'categories': categories,
        'recent_products': recent_products,
        'scans_today': scans_today,
        'scan_history': scan_history,
    }
    
    return render(request, 'inventory/dashboard.html', context)

@login_required
def barcode_scanner(request):
    """Barcode scanner view"""
    return render(request, 'inventory/barcode_scanner.html')

@login_required
def kanban_board(request):
    """Kanban board view"""
    categories = Category.objects.all()
    return render(request, 'inventory/kanban_board.html', {'categories': categories})

def fetch_product_data(barcode):
    """Fetch product data from external API with timeout"""
    try:
        # Set a timeout of 5 seconds for the API call
        response = requests.get(f'https://products-test-aci.onrender.com/product/{barcode}', timeout=5)
        if response.status_code == 200:
            return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"API Error: {str(e)}")
    
    # Return default product data if API fails
    return {
        'name': f'Product {barcode}',
        'description': 'No description available',
        'price': None,
        'image_url': None
    }

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_product(request):
    """API to add a product from barcode scan"""
    try:
        data = json.loads(request.body)
        barcode = data.get('barcode')
        
        if not barcode:
            return JsonResponse({'status': 'error', 'message': 'Barcode is required'}, status=400)
        
        # Check if product already exists
        try:
            existing_product = Product.objects.get(barcode=barcode)
            # Record the scan
            ProductScan(product=existing_product).save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Product already exists in inventory',
                'product': {
                    'id': str(existing_product.id),
                    'name': existing_product.name,
                    'barcode': existing_product.barcode,
                    'category': existing_product.category.name,
                    'description': existing_product.description,
                    'price': str(existing_product.price) if existing_product.price else None,
                    'image_url': existing_product.image_url
                }
            })
        except DoesNotExist:
            # Product doesn't exist, continue to create it
            pass
        
        # Use ThreadPoolExecutor to fetch product data with a timeout
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(fetch_product_data, barcode)
            try:
                product_data = future.result(timeout=5)  # 5 second timeout
            except concurrent.futures.TimeoutError:
                product_data = {
                    'name': f'Product {barcode}',
                    'description': 'No description available',
                    'price': None,
                    'image_url': None
                }
            
        # Get or create uncategorized category
        try:
            uncategorized = Category.objects.get(name="Uncategorized")
        except DoesNotExist:
            uncategorized = Category(name="Uncategorized")
            uncategorized.save()
        
        # Create product
        product = Product(
            name=product_data.get('name', f'Product {barcode}'),
            barcode=barcode,
            category=uncategorized,
            description=product_data.get('description', ''),
            price=product_data.get('price'),
            image_url=product_data.get('image_url')
        )
        product.save()
        
        # Record the scan
        ProductScan(product=product).save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product added successfully',
            'product': {
                'id': str(product.id),
                'name': product.name,
                'barcode': product.barcode,
                'category': product.category.name,
                'description': product.description,
                'price': str(product.price) if product.price else None,
                'image_url': product.image_url
            }
        })
            
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': f'Validation error: {str(e)}'}, status=400)
    except NotUniqueError:
        return JsonResponse({'status': 'error', 'message': 'Product with this barcode already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def get_products(request):
    """API to get all products, optionally filtered by category"""
    try:
        category_id = request.GET.get('category_id')
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                products = Product.objects(category=category)
            except DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)
        else:
            products = Product.objects.all()
            
        products_data = []
        for product in products:
            products_data.append({
                'id': str(product.id),
                'name': product.name,
                'barcode': product.barcode,
                'category_id': str(product.category.id),
                'category_name': product.category.name,
                'description': product.description,
                'price': str(product.price) if product.price else None,
                'image_url': product.image_url,
                'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        return JsonResponse({'status': 'success', 'products': products_data})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def update_category(request, product_id):
    """API to update product category"""
    try:
        # Validate the product_id is a valid ObjectId
        try:
            if not ObjectId.is_valid(product_id):
                return JsonResponse({'status': 'error', 'message': 'Invalid product ID format'}, status=400)
            
            # Convert string ID to ObjectId
            product_object_id = ObjectId(product_id)
            product = Product.objects.get(id=product_object_id)
        except (DoesNotExist, bson_errors.InvalidId):
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
            
        data = json.loads(request.body)
        category_id = data.get('category_id')
        
        if not category_id:
            return JsonResponse({'status': 'error', 'message': 'Category ID is required'}, status=400)
            
        try:
            if not ObjectId.is_valid(category_id):
                return JsonResponse({'status': 'error', 'message': 'Invalid category ID format'}, status=400)
                
            # Convert string ID to ObjectId
            category_object_id = ObjectId(category_id)
            category = Category.objects.get(id=category_object_id)
        except (DoesNotExist, bson_errors.InvalidId):
            return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)
            
        product.category = category
        product.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Product category updated successfully',
            'product': {
                'id': str(product.id),
                'name': product.name,
                'category_id': str(product.category.id),
                'category_name': product.category.name
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_category(request):
    """API to add a new category"""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Category name is required'}, status=400)
            
        # Check if category already exists
        try:
            Category.objects.get(name=name)
            return JsonResponse({'status': 'error', 'message': 'Category with this name already exists'}, status=400)
        except DoesNotExist:
            pass
            
        category = Category(name=name)
        category.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Category added successfully',
            'category': {
                'id': str(category.id),
                'name': category.name
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': f'Validation error: {str(e)}'}, status=400)
    except NotUniqueError:
        return JsonResponse({'status': 'error', 'message': 'Category with this name already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def get_categories(request):
    """API to get all categories"""
    try:
        categories = Category.objects.all()
        categories_data = []
        
        for category in categories:
            product_count = Product.objects(category=category).count()
            categories_data.append({
                'id': str(category.id),
                'name': category.name,
                'product_count': product_count
            })
            
        return JsonResponse({'status': 'success', 'categories': categories_data})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    """API to delete a product"""
    try:
        # Validate the product_id is a valid ObjectId
        if not ObjectId.is_valid(product_id):
            return JsonResponse({'status': 'error', 'message': 'Invalid product ID format'}, status=400)
        
        # Convert string ID to ObjectId
        product_object_id = ObjectId(product_id)
        
        try:
            product = Product.objects.get(id=product_object_id)
            product_name = product.name
            
            # Delete the product (this will also delete associated scans due to CASCADE)
            product.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Product "{product_name}" deleted successfully'
            })
        except DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    """API to delete a category"""
    try:
        # Validate the category_id is a valid ObjectId
        if not ObjectId.is_valid(category_id):
            return JsonResponse({'status': 'error', 'message': 'Invalid category ID format'}, status=400)
        
        # Convert string ID to ObjectId
        category_object_id = ObjectId(category_id)
        
        try:
            category = Category.objects.get(id=category_object_id)
            
            # Don't allow deleting the Uncategorized category
            if category.name == "Uncategorized":
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot delete the Uncategorized category'
                }, status=400)
            
            # Check if category has products
            product_count = Product.objects(category=category).count()
            if product_count > 0:
                # Get the Uncategorized category
                try:
                    uncategorized = Category.objects.get(name="Uncategorized")
                except DoesNotExist:
                    # Create it if it doesn't exist
                    uncategorized = Category(name="Uncategorized")
                    uncategorized.save()
                
                # Move all products to Uncategorized
                Product.objects(category=category).update(category=uncategorized)
            
            # Delete the category
            category_name = category.name
            category.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Category "{category_name}" deleted successfully',
                'moved_products': product_count > 0,
                'product_count': product_count
            })
        except DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def update_category_details(request, category_id):
    """API to update category details"""
    try:
        # Validate the category_id is a valid ObjectId
        if not ObjectId.is_valid(category_id):
            return JsonResponse({'status': 'error', 'message': 'Invalid category ID format'}, status=400)
        
        # Convert string ID to ObjectId
        category_object_id = ObjectId(category_id)
        
        try:
            category = Category.objects.get(id=category_object_id)
            
            # Don't allow renaming the Uncategorized category
            if category.name == "Uncategorized":
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot rename the Uncategorized category'
                }, status=400)
            
            data = json.loads(request.body)
            name = data.get('name')
            
            if not name:
                return JsonResponse({'status': 'error', 'message': 'Category name is required'}, status=400)
            
            # Check if another category with this name exists
            try:
                existing_category = Category.objects.get(name=name)
                if str(existing_category.id) != category_id:
                    return JsonResponse({'status': 'error', 'message': 'Category with this name already exists'}, status=400)
            except DoesNotExist:
                pass
            
            # Update category
            old_name = category.name
            category.name = name
            category.save()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Category updated from "{old_name}" to "{name}"',
                'category': {
                    'id': str(category.id),
                    'name': category.name
                }
            })
        except DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': f'Validation error: {str(e)}'}, status=400)
    except NotUniqueError:
        return JsonResponse({'status': 'error', 'message': 'Category with this name already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
