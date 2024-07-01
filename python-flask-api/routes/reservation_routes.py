from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

reservation_bp = Blueprint('reservation_bp', __name__)
mysql = MySQL()

@reservation_bp.route('/reservations', methods=['GET'])
def get_reservations():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Reservation")
    reservations = cursor.fetchall()
    return jsonify(reservations)

@reservation_bp.route('/reservations/<int:id>', methods=['GET'])
def get_reservation_by_id(id: int):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Reservation WHERE ReservationID = %s", (id,))
    reservation = cursor.fetchone()
    if reservation is None:
        return jsonify({'error': 'Reservation does not exist'}), 404
    return jsonify(reservation)

@reservation_bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    customer_id = data['customer_id']
    reservation_date = data['reservation_date']
    number_of_people = data['number_of_people']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Reservation (RestaurantID, CustomerID, ReservationDate, NumberOfPeople) VALUES (%s, %s, %s, %s)", (restaurant_id, customer_id, reservation_date, number_of_people))
    mysql.connection.commit()
    return '', 201

@reservation_bp.route('/reservations/<int:id>', methods=['PUT'])
def update_reservation(id: int):
    data = request.get_json()
    reservation_date = data['reservation_date']
    number_of_people = data['number_of_people']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Reservation SET ReservationDate = %s, NumberOfPeople = %s WHERE ReservationID = %s", (reservation_date, number_of_people, id))
    mysql.connection.commit()
    return '', 200

@reservation_bp.route('/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Reservation WHERE ReservationID = %s", (id,))
    mysql.connection.commit()
    return '', 200
