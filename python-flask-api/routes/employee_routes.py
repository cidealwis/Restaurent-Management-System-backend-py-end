from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

employee_bp = Blueprint('employee_bp', __name__)
mysql = MySQL()

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    return jsonify(employees)

@employee_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Employee WHERE EmployeeID = %s", (id,))
    employee = cursor.fetchone()
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)

@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    name = data['name']
    position = data['position']
    phone_number = data['phone_number']
    email = data['email']
    manager_id = data.get('manager_id')
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Employee (RestaurantID, Name, Position, PhoneNumber, Email, ManagerID) VALUES (%s, %s, %s, %s, %s, %s)", (restaurant_id, name, position, phone_number, email, manager_id))
    mysql.connection.commit()
    return '', 201

@employee_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    name = data['name']
    position = data['position']
    phone_number = data['phone_number']
    email = data['email']
    manager_id = data.get('manager_id')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Employee SET RestaurantID = %s, Name = %s, Position = %s, PhoneNumber = %s, Email = %s, ManagerID = %s WHERE EmployeeID = %s", (restaurant_id, name, position, phone_number, email, manager_id, id))
    mysql.connection.commit()
    return '', 200

@employee_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Employee WHERE EmployeeID = %s", (id,))
    mysql.connection.commit()
    return '', 200
