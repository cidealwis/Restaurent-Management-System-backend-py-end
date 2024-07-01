from flask import Blueprint

# Import individual route blueprints
from .restaurant_routes import restaurant_bp
from .reservation_routes import reservation_bp
from .employee_routes import employee_bp
from .menu_item_routes import menu_item_bp
from .menu_routes import menu_bp
from .order_item_routes import order_item_bp
from .order_routes import order_bp
from .customer_routes import customer_bp
