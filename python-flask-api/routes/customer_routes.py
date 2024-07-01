from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

customer_bp = Blueprint('customer_bp', __name__)
mysql = MySQL()

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    return jsonify(customers)

@customer_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (id,))
    customer = cursor.fetchone()
    if customer is None:
        return jsonify({'error': 'Customer does not exist'}), 404
    return jsonify(customer)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data['name']
    phone_number = data['phone_number']
    email = data['email']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Customer (Name, PhoneNumber, Email) VALUES (%s, %s, %s)", (name, phone_number, email))
    mysql.connection.commit()
    return '', 201

@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id: int):
    data = request.get_json()
    name = data['name']
    phone_number = data['phone_number']
    email = data['email']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Customer SET Name = %s, PhoneNumber = %s, Email = %s WHERE CustomerID = %s", (name, phone_number, email, id))
    mysql.connection.commit()
    return '', 200

@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", (id,))
    mysql.connection.commit()
    return '', 200
