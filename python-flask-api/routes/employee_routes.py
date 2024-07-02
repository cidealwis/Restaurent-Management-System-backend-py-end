from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging  
logging.basicConfig(level=logging.DEBUG)

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
    manager_id = data.get('manager_id')  # Use .get() to handle optional fields

    try:
        cursor = mysql.connection.cursor()
        if manager_id:
            cursor.execute("INSERT INTO Employee (RestaurantID, Name, Position, PhoneNumber, Email, ManagerID) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (restaurant_id, name, position, phone_number, email, manager_id))
        else:
            cursor.execute("INSERT INTO Employee (RestaurantID, Name, Position, PhoneNumber, Email) VALUES (%s, %s, %s, %s, %s)", 
                           (restaurant_id, name, position, phone_number, email))
        mysql.connection.commit()
        return jsonify({'message': 'Employee created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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

@employee_bp.route('/employees/login', methods=['POST'])
def login_employee():
    try:
        data = request.get_json()
        email = data.get('email')
        phone_number = data.get('phone_number')
        restaurant_id = data.get('restaurant_id')
        manager_id = data.get('manager_id')
        
        logging.debug(f"Attempting to login with email: {email} and phone number: {phone_number}")
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Employee WHERE Email = %s AND PhoneNumber = %s", (email, phone_number))
        employee = cursor.fetchone()
        
        logging.debug(f"Employee found: {employee}")
        
        if employee:
            # Add restaurant_id and manager_id to employee data before returning
            employee['RestaurantID'] = restaurant_id
            employee['ManagerID'] = manager_id
            
            return jsonify({'message': 'Login successful', 'employee': employee}), 200
        else:
            logging.error("Invalid email or phone number")
            return jsonify({'error': 'Invalid email or phone number'}), 401
    except Exception as e:
        logging.error(f"Exception occurred during login: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500