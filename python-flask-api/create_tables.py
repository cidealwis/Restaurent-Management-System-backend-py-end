import MySQLdb
from config import Config

def create_tables():
    db = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB
    )
    cursor = db.cursor()

    tables = {
        'Restaurants': '''
            CREATE TABLE IF NOT EXISTS Restaurants (
                RestaurantID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Address VARCHAR(255),
                PhoneNumber VARCHAR(20),
                Email VARCHAR(255)
            )
        ''',
        'Menu': '''
            CREATE TABLE IF NOT EXISTS Menu (
                MenuID INT AUTO_INCREMENT PRIMARY KEY,
                RestaurantID INT,
                Name VARCHAR(255) NOT NULL,
                Description TEXT,
                FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
            )
        ''',
        'MenuItem': '''
            CREATE TABLE IF NOT EXISTS MenuItem (
                MenuItemID INT AUTO_INCREMENT PRIMARY KEY,
                MenuID INT,
                Name VARCHAR(255) NOT NULL,
                Description TEXT,
                Price DECIMAL(10, 2),
                FOREIGN KEY (MenuID) REFERENCES Menu(MenuID)
            )
        ''',
        'Employee': '''
            CREATE TABLE IF NOT EXISTS Employee (
                EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
                RestaurantID INT,
                Name VARCHAR(255) NOT NULL,
                Position VARCHAR(255),
                PhoneNumber VARCHAR(20),
                Email VARCHAR(255),
                ManagerID INT,
                FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
                FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
            )
        ''',
        'Customer': '''
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                PhoneNumber VARCHAR(20),
                Email VARCHAR(255)
            )
        ''',
        'CustomerAddresses': '''
            CREATE TABLE IF NOT EXISTS CustomerAddresses (
                CustomerID INT,
                Address VARCHAR(255),
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            )
        ''',
        'Reservation': '''
            CREATE TABLE IF NOT EXISTS Reservation (
                ReservationID INT AUTO_INCREMENT PRIMARY KEY,
                RestaurantID INT,
                CustomerID INT,
                ReservationDate DATETIME,
                NumberOfPeople INT,
                ReservationStatus VARCHAR(255),
                FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            )
        ''',
        'Order': '''
            CREATE TABLE IF NOT EXISTS `Order` (
                OrderID INT AUTO_INCREMENT PRIMARY KEY,
                RestaurantID INT,
                CustomerID INT,
                EmployeeID INT,
                OrderDate DATETIME,
                TotalAmount DECIMAL(10, 2),
                FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
            )
        ''',
        'OrderItem': '''
            CREATE TABLE IF NOT EXISTS OrderItem (
                OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
                OrderID INT,
                MenuItemID INT,
                Quantity INT,
                Price DECIMAL(10, 2),
                FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
                FOREIGN KEY (MenuItemID) REFERENCES MenuItem(MenuItemID)
            )
        '''
    }

    for table_name, table_sql in tables.items():
        try:
            cursor.execute(table_sql)
            print(f"Table {table_name} created successfully.")
        except MySQLdb.Error as err:
            print(f"Error creating table {table_name}: {err}")

    db.commit()
    db.close()

if __name__ == '__main__':
    create_tables()
