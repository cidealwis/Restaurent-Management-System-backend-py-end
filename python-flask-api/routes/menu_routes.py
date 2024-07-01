from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

menu_bp = Blueprint('menu_bp', __name__)
mysql = MySQL()

@menu_bp.route('/menus', methods=['GET'])
def get_menus():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Menu")
    menus = cursor.fetchall()
    return jsonify(menus)

@menu_bp.route('/menus/<int:id>', methods=['GET'])
def get_menu_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Menu WHERE MenuID = %s", (id,))
    menu = cursor.fetchone()
    if menu is None:
        return jsonify({'error': 'Menu does not exist'}), 404
    return jsonify(menu)

@menu_bp.route('/menus', methods=['POST'])
def create_menu():
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    name = data['name']
    description = data['description']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Menu (RestaurantID, Name, Description) VALUES (%s, %s, %s)", (restaurant_id, name, description))
    mysql.connection.commit()
    return '', 201

@menu_bp.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id: int):
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    name = data['name']
    description = data['description']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Menu SET RestaurantID = %s, Name = %s, Description = %s WHERE MenuID = %s", (restaurant_id, name, description, id))
    mysql.connection.commit()
    return '', 200

@menu_bp.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Menu WHERE MenuID = %s", (id,))
    mysql.connection.commit()
    return '', 200
