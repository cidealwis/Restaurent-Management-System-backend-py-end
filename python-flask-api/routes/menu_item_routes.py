from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

menu_item_bp = Blueprint('menu_item_bp', __name__)
mysql = MySQL()

@menu_item_bp.route('/menu_items', methods=['GET'])
def get_menu_items():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM MenuItem")
    menu_items = cursor.fetchall()
    return jsonify(menu_items)

@menu_item_bp.route('/menu_items/<int:id>', methods=['GET'])
def get_menu_item_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM MenuItem WHERE MenuItemID = %s", (id,))
    menu_item = cursor.fetchone()
    if menu_item is None:
        return jsonify({'error': 'Menu item does not exist'}), 404
    return jsonify(menu_item)

@menu_item_bp.route('/menu_items', methods=['POST'])
def create_menu_item():
    data = request.get_json()
    menu_id = data['menu_id']
    name = data['name']
    description = data['description']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO MenuItem (MenuID, Name, Description, Price) VALUES (%s, %s, %s, %s)", (menu_id, name, description, price))
    mysql.connection.commit()
    return '', 201

@menu_item_bp.route('/menu_items/<int:id>', methods=['PUT'])
def update_menu_item(id: int):
    data = request.get_json()
    menu_id = data['menu_id']
    name = data['name']
    description = data['description']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE MenuItem SET MenuID = %s, Name = %s, Description = %s, Price = %s WHERE MenuItemID = %s", (menu_id, name, description, price, id))
    mysql.connection.commit()
    return '', 200

@menu_item_bp.route('/menu_items/<int:id>', methods=['DELETE'])
def delete_menu_item(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM MenuItem WHERE MenuItemID = %s", (id,))
    mysql.connection.commit()
    return '', 200
