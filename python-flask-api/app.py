from flask import Flask
from flask_mysqldb import MySQL
from config import Config 

app = Flask(__name__)

app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Import and register blueprints from routes package
from routes import *

app.register_blueprint(restaurant_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(menu_item_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_item_bp)
app.register_blueprint(order_bp)
app.register_blueprint(customer_bp)

if __name__ == '__main__':
    app.run(port=5000)
