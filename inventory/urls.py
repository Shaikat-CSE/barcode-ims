from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('barcode-scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('kanban-board/', views.kanban_board, name='kanban_board'),
    
    # API endpoints
    path('api/add-product/', views.add_product, name='add_product'),
    path('api/products/', views.get_products, name='get_products'),
    path('api/update-category/<str:product_id>/', views.update_category, name='update_category'),
    path('api/add-category/', views.add_category, name='add_category'),
    path('api/categories/', views.get_categories, name='get_categories'),
    
    # New API endpoints for deletion and editing
    path('api/delete-product/<str:product_id>/', views.delete_product, name='delete_product'),
    path('api/delete-category/<str:category_id>/', views.delete_category, name='delete_category'),
    path('api/update-category-details/<str:category_id>/', views.update_category_details, name='update_category_details'),
] 