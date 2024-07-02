from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

restaurant_bp = Blueprint('restaurant_bp', __name__)
mysql = MySQL()

@restaurant_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Restaurants")
    restaurants = cursor.fetchall()
    return jsonify(restaurants)

@restaurant_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Restaurants WHERE RestaurantID = %s", (id,))
    restaurant = cursor.fetchone()
    if restaurant is None:
        return jsonify({'error': 'Restaurants does not exist'}), 404
    return jsonify(restaurant)

@restaurant_bp.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    name = data['name']
    address = data['address']
    phone_number = data['phone_number']
    email = data['email']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Restaurants (Name, Address, PhoneNumber, Email) VALUES (%s, %s, %s, %s)", (name, address, phone_number, email))
    mysql.connection.commit()
    return "success", 201

@restaurant_bp.route('/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id: int):
    data = request.get_json()
    name = data['name']
    address = data['address']
    phone_number = data['phone_number']
    email = data['email']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Restaurants SET Name = %s, Address = %s, PhoneNumber = %s, Email = %s WHERE RestaurantID = %s", (name, address, phone_number, email, id))
    mysql.connection.commit()
    return '', 200

@restaurant_bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Restaurants WHERE RestaurantID = %s", (id,))
    mysql.connection.commit()
    return '', 200

@restaurant_bp.route('/restaurants/login', methods=['POST'])
def restaurant_login():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')

    if not email or not phone:
        return jsonify({'error': 'Email and phone number are required.'}), 400

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Restaurants WHERE Email = %s AND PhoneNumber = %s", (email, phone))
        restaurant = cursor.fetchone()

        if restaurant:
            # Construct the response JSON object with relevant data
            response_data = {
                'message': 'Login successful.',
                'restaurant': {
                    'id': restaurant['RestaurantID'],
                    'name': restaurant['Name'],
                    'email': restaurant['Email'],
                    'phone_number': restaurant['PhoneNumber']
                    # Add other fields as needed
                }
            }
            return jsonify(response_data), 200
        else:
            return jsonify({'error': 'Invalid credentials. Please check your email and phone number.'}), 401

    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500