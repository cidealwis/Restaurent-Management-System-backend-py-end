from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

order_bp = Blueprint('order_bp', __name__)
mysql = MySQL()

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `Order`")
    orders = cursor.fetchall()
    return jsonify(orders)

@order_bp.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `Order` WHERE OrderID = %s", (id,))
    order = cursor.fetchone()
    if order is None:
        return jsonify({'error': 'Order does not exist'}), 404
    return jsonify(order)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    customer_id = data['customer_id']
    employee_id = data['employee_id']
    order_date = data['order_date']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO `Order` (RestaurantID, CustomerID, EmployeeID, OrderDate) VALUES (%s, %s, %s, %s)", (restaurant_id, customer_id, employee_id, order_date))
    mysql.connection.commit()
    return '', 201

@order_bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id: int):
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    customer_id = data['customer_id']
    employee_id = data['employee_id']
    order_date = data['order_date']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE `Order` SET RestaurantID = %s, CustomerID = %s, EmployeeID = %s, OrderDate = %s WHERE OrderID = %s", (restaurant_id, customer_id, employee_id, order_date, id))
    mysql.connection.commit()
    return '', 200

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM `Order` WHERE OrderID = %s", (id,))
    mysql.connection.commit()
    return '', 200
