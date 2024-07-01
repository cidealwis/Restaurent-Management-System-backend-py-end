from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

order_item_bp = Blueprint('order_item_bp', __name__)
mysql = MySQL()

@order_item_bp.route('/order_items', methods=['GET'])
def get_order_items():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM OrderItem")
    order_items = cursor.fetchall()
    return jsonify(order_items)

@order_item_bp.route('/order_items/<int:id>', methods=['GET'])
def get_order_item_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM OrderItem WHERE OrderItemID = %s", (id,))
    order_item = cursor.fetchone()
    if order_item is None:
        return jsonify({'error': 'OrderItem does not exist'}), 404
    return jsonify(order_item)

@order_item_bp.route('/order_items', methods=['POST'])
def create_order_item():
    data = request.get_json()
    order_id = data['order_id']
    menu_item_id = data['menu_item_id']
    quantity = data['quantity']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO OrderItem (OrderID, MenuItemID, Quantity, Price) VALUES (%s, %s, %s, %s)", (order_id, menu_item_id, quantity, price))
    mysql.connection.commit()
    return '', 201

@order_item_bp.route('/order_items/<int:id>', methods=['PUT'])
def update_order_item(id: int):
    data = request.get_json()
    quantity = data['quantity']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE OrderItem SET Quantity = %s, Price = %s WHERE OrderItemID = %s", (quantity, price, id))
    mysql.connection.commit()
    return '', 200

@order_item_bp.route('/order_items/<int:id>', methods=['DELETE'])
def delete_order_item(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM OrderItem WHERE OrderItemID = %s", (id,))
    mysql.connection.commit()
    return '', 200
