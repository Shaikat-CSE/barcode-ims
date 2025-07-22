# Barcode-Driven Inventory Management System

A responsive and modern inventory management system that uses barcode scanning to add products and a drag-and-drop kanban board to organize them by category.

![Barcode IMS](https://via.placeholder.com/800x400?text=Barcode+Inventory+Management+System)

## Features

- **Barcode Scanner**: Scan product barcodes using your device's camera or enter them manually
- **Product Lookup**: Automatically fetch product details from an external API
- **Kanban Board**: Organize products by category using drag-and-drop functionality
- **Analytics Dashboard**: View product statistics, category distribution, and scan activity
- **Responsive Design**: Works on desktop and mobile devices
- **User Authentication**: Secure login and registration system
- **Product & Category Management**: Add, edit, and delete products and categories

## Tech Stack

### Backend
- **Django (5.0+)**: High-level Python web framework that encourages rapid development and clean, pragmatic design
  - Handles URL routing, views, templating, forms, and admin interface
  - Provides the core structure for the application

### Database
- **MongoDB (via MongoEngine)**: NoSQL document database used for flexible schema design
  - Stores product, category, user, and scanning data
  - Allows for easy scaling and schema evolution
  - Hosted on MongoDB Atlas for reliability and easy scaling

### Frontend
- **Django Templates**: Server-side template rendering
- **Bootstrap 5**: CSS framework for responsive layouts and UI components
- **Vanilla JavaScript**: Custom client-side interactivity
- **SortableJS**: Library for drag-and-drop functionality in the kanban board
- **HTML5-QRCode**: JavaScript library for barcode scanning via device camera
- **SweetAlert2**: Library for enhanced dialog boxes and notifications
- **Chart.js**: JavaScript library for creating interactive charts in the analytics dashboard

### Deployment & DevOps
- **Render**: Cloud platform for hosting the application
- **Gunicorn**: WSGI HTTP server for running Django in production
- **WhiteNoise**: Library for serving static files directly from Django
- **Python-Decouple**: Library for separating configuration from code

### Security
- **Django's Authentication System**: For handling user authentication and sessions
- **CSRF Protection**: Prevents cross-site request forgery attacks
- **Environment Variables**: Securely stores sensitive information like API keys and database credentials

## Why This Tech Stack?

- **Django**: Chosen for its "batteries-included" philosophy, robust ORM, built-in admin, and security features
- **MongoDB**: Selected over SQL databases for its flexibility, horizontal scalability, and document-oriented structure that aligns well with the variable product attributes
- **MongoEngine**: Provides a Document-Object Mapper for MongoDB, making it easier to work with MongoDB in a Django project
- **Bootstrap 5**: Enables rapid UI development with responsive design out of the box
- **Vanilla JavaScript**: Used for custom interactivity without the overhead of a heavy framework, since the application's frontend needs are relatively straightforward
- **SortableJS**: Lightweight, touch-friendly library specifically designed for drag-and-drop interfaces
- **Render**: Selected for its ease of deployment, built-in CI/CD, and free tier suitable for smaller applications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shaikat-CSE/barcode-ims.git
cd barcode-ims
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   MONGODB_URI=your-mongodb-connection-string
   ```

4. Initialize the database with sample data:
```bash
python manage.py init_mongodb
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application at http://localhost:8000

## Deployment to Render

### Prerequisites
- A [Render](https://render.com/) account
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account with a database set up

### Steps

1. Push your code to GitHub or GitLab.

2. In Render:
   - Create a new Web Service
   - Connect to your repository
   - Select "Python" as the environment
   - Set the build command to `./build.sh`
   - Set the start command to `gunicorn inventory_system.wsgi:application`
   - Add the following environment variables:
     - `SECRET_KEY`: A secure random string
     - `DEBUG`: `false`
     - `ALLOWED_HOSTS`: Include your Render domain, e.g., `render.com,*.onrender.com`
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `SECURE_SSL_REDIRECT`: `true`
     - `SESSION_COOKIE_SECURE`: `true`
     - `CSRF_COOKIE_SECURE`: `true`

3. Alternatively, if you have the Render CLI installed:
   ```bash
   render deploy
   ```
   This will use the included `render.yaml` configuration file.

## MongoDB Integration

This application uses MongoDB as the database backend through MongoEngine, which provides a Document-Object Mapper (similar to Django's ORM) for MongoDB. The main benefits include:

- **Schema Flexibility**: MongoDB's document model allows for flexible schemas
- **Scalability**: MongoDB is designed to scale horizontally
- **Performance**: MongoDB provides high performance for read and write operations
- **Cloud Hosting**: MongoDB Atlas provides a fully managed cloud database service

## API Endpoints

- `POST /api/add-product/`: Add a new product from barcode
- `GET /api/products/`: Get all products (optionally filtered by category)
- `PATCH /api/update-category/<product_id>/`: Update a product's category
- `POST /api/add-category/`: Add a new category
- `GET /api/categories/`: Get all categories
- `DELETE /api/delete-product/<product_id>/`: Delete a product
- `DELETE /api/delete-category/<category_id>/`: Delete a category
- `PATCH /api/update-category-details/<category_id>/`: Update category details

## Project Structure

```
barcode-ims/
├── accounts/                # User authentication app
├── inventory/               # Main application for inventory management
├── inventory_system/        # Django project settings
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── build.sh                 # Build script for Render deployment
├── manage.py                # Django management script
├── README.md                # Project documentation
├── render.yaml              # Render deployment configuration
└── requirements.txt         # Python dependencies
```

## Best Practices Implemented

- **Environment Variables**: Sensitive information is stored in environment variables
- **Separation of Concerns**: Code is organized into distinct apps based on functionality
- **Security Measures**: HTTPS enforcement, secure cookies, and CSRF protection
- **Comprehensive Documentation**: Detailed README with setup and deployment instructions
- **Clean Code**: Following PEP 8 style guide for Python code
- **Optimized Static Files**: WhiteNoise for efficient static file serving
- **Responsive Design**: Bootstrap for mobile-friendly interfaces
- **Error Handling**: Proper exception handling and user-friendly error messages
- **Deployment Configuration**: Included configuration files for easy deployment

## Developer

This project was developed by **Shaikat Sharma**. 

## License

This project is licensed under the MIT License - see the LICENSE file for details. 