# Ecommerce Platform

A modern e-commerce web application built with Django, featuring product management, shopping cart functionality, and user authentication.

## Features

- **User Authentication**: Registration, login, and profile management
- **Product Catalog**: Browse products by category (Gents Pants, Sarees, Borkhas, Lehengas, Baby Fashion)
- **Shopping Cart**: Add/remove items, update quantities with AJAX
- **Order Management**: Place orders and manage purchase history
- **User Profile**: Update personal and delivery information
- **Password Management**: Change password with security reset functionality
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Project Structure

```
Ecommerce/
├── Ecommerce/              # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── Shop/                   # Main app
│   ├── models.py           # Database models (Product, Customer, Cart, OrderPlaced)
│   ├── views.py            # View functions and classes
│   ├── urls.py             # App URL patterns
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin configuration
│   ├── static/             # CSS, JS, images
│   └── templates/          # HTML templates
├── media/                  # User-uploaded files
├── manage.py               # Django management commands
└── db.sqlite3              # Database file
```

## Technologies Used

- **Backend**: Django 5.2.5
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Image Processing**: Pillow (PIL)
- **AJAX**: jQuery for async requests
- **Other**: Django Forms, Authentication

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/alamindev25/Ecommerce_ponnoala.git
   cd Ecommerce
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # macOS/Linux
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt doesn't exist, install these packages:
   ```bash
   pip install Django==5.2.5
   pip install Pillow==11.3.0
   pip install sqlparse==0.5.3
   pip install asgiref==3.9.1
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Customers
1. Register a new account or login
2. Browse products by category (Gents Pants, Sarees, Borkhas, Lehengas, Baby Fashion)
3. Click on products to view details
4. Add items to cart using the "Add to Cart" button
5. View cart, adjust quantities, and remove items
6. Update profile with delivery address
7. Place order and track order history

### For Administrators
1. Login to admin panel: http://127.0.0.1:8000/admin/
2. Manage products, customers, and orders
3. View and update order status
4. Manage product categories and pricing

## API Endpoints

### Cart Operations (AJAX)
- `GET /pluscart/` - Increase item quantity
- `GET /minuscart/` - Decrease item quantity
- `GET /removecart/` - Remove item from cart

Parameters: `prod_id` (product ID)

### Main URLs
- `/` - Home page
- `/product-detail/<id>` - Product detail page
- `/cart/` - Shopping cart
- `/add_to_cart/` - Add product to cart
- `/profile/` - User profile
- `/address/` - Manage addresses
- `/registration/` - User registration
- `/accounts/login/` - Login
- `/logout/` - Logout
- `/lehenga/` - Lehenga category
- `/passwordchange/` - Change password

## Database Models

### Product
- Product ID, Title, Description
- Selling Price, Discounted Price
- Category, Brand
- Product Image

### Customer
- User (ForeignKey to User)
- Name, Phone, Address Details
- Division, District, Thana, Zipcode

### Cart
- User, Product (ForeignKey)
- Quantity, Created Date

### OrderPlaced
- User, Product
- Quantity, Ordered Date
- Status, Payment Method

## Development Notes

### Static Files
- CSS: `Shop/static/Shop/css/`
- JavaScript: `Shop/static/Shop/js/`
- Images: `Shop/static/Shop/images/`

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Run Tests
```bash
python manage.py test
```

## Common Issues & Solutions

### Issue: MultiValueDictKeyError for 'pid' or 'prod_id'
**Solution**: Ensure JavaScript is sending the correct parameter name to the AJAX endpoint.

### Issue: Static files not loading
**Solution**: 
```bash
python manage.py collectstatic --noinput
```

### Issue: Images not displaying
**Solution**: Ensure `MEDIA_URL` and `MEDIA_ROOT` are correctly configured in settings.py

### Issue: Database locked
**Solution**: Delete `db.sqlite3` and run migrations again:
```bash
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

- [ ] Payment Gateway Integration (Stripe, SSLCommerz)
- [ ] Email notifications
- [ ] Product reviews and ratings
- [ ] Wishlist feature
- [ ] Advanced search and filtering
- [ ] Admin dashboard with analytics
- [ ] Inventory management
- [ ] Multiple payment methods
- [ ] Order tracking with SMS updates

## License

This project is open source and available under the MIT License.

## Support & Contact

For issues, questions, or suggestions, please create an issue in the GitHub repository or contact the maintainers.

---

**Happy Shopping! 🛍️**
