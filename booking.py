import pyodbc
from Options import *
from Login import *
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt

class BookingScreen(QtWidgets.QMainWindow):
    def __init__(self, from_city, to_city, out_date, class_name,booking_id ,connection_string, return_date=None):
        super().__init__()
        uic.loadUi("booking.ui", self)

        self.connection_string = connection_string
        self.from_city = from_city
        self.to_city = to_city
        self.out_date = out_date
        self.booking_id=booking_id
        self.return_date = return_date
        self.class_name = class_name
        self.book1.clicked.connect(self.proceed)
        self.book2.clicked.connect(self.proceed)


        # Database connection

        self.load_flights()

    def get_connection(self):
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Cannot connect to database:\n{str(e)}")
            return None

    def load_flights(self):
        conn = self.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        results = []

        # Clear previous table content
        self.flight_list.clear()
        self.flight_list.setRowCount(0)

        # Query for one-way or round-trip flights
        # FIXED: Now matching the exact format "Airport Name, City Name"
        query = """
        SELECT 
            f.FlightID,
            fs.ScheduleID,
            fs.DepartureTime,
            fs.ArrivalTime,
            a_dep.Name + ' (' + a_dep.Code + ')' AS FromAirport,
            a_arr.Name + ' (' + a_arr.Code + ')' AS ToAirport,
            (f.BaseFare * cl.ClassMultiplier) AS Price,
            a.Capacity - ISNULL(COUNT(b.BookingID), 0) AS AvailableSeats,
            fs.Duration
        FROM Flight f
        JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
        JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
        JOIN Cities c_dep ON a_dep.CityID = c_dep.CityID
        JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
        JOIN Cities c_arr ON a_arr.CityID = c_arr.CityID
        JOIN FlightClass fc ON f.FlightID = fc.FlightID
        JOIN Class cl ON fc.ClassID = cl.ClassID
        JOIN Aircraft a ON f.AircraftID = a.AircraftID
        LEFT JOIN Booking b 
            ON b.ScheduleID = fs.ScheduleID
            AND b.ClassID = cl.ClassID
            AND b.Status <> 'cancelled'
        WHERE 
            CONCAT(a_dep.Name, ', ', c_dep.CityName) = ?
            AND CONCAT(a_arr.Name, ', ', c_arr.CityName) = ?
            AND fs.DepartureDate = ?
            AND cl.ClassName = ?
            AND fs.Status = 'scheduled'
        GROUP BY 
            f.FlightID, fs.ScheduleID, fs.DepartureTime, fs.ArrivalTime,
            a_dep.Name, a_dep.Code, a_arr.Name, a_arr.Code, f.BaseFare, cl.ClassMultiplier,
            a.Capacity, fs.Duration
        HAVING 
            a.Capacity - ISNULL(COUNT(b.BookingID), 0) > 0
        ORDER BY Price
        """

        # Execute with parameters from search.py
        cursor.execute(query, (self.from_city, self.to_city, self.out_date, self.class_name))
        results = cursor.fetchall()
        conn.close()

        if not results:
            self.label_6.setText("No flights available")
            return

        # Populate QTableWidget
        self.flight_list.setColumnCount(9)
        self.flight_list.setHorizontalHeaderLabels([
            "Flight ID", "Schedule ID", "Departure", "Arrival", 
            "From Airport", "To Airport", "Price", "Available Seats", "Duration"
        ])
        self.flight_list.setRowCount(len(results))

        for row_idx, row_data in enumerate(results):
            self.flight_list.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.flight_list.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
            self.flight_list.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))
            self.flight_list.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3])))
            self.flight_list.setItem(row_idx, 4, QTableWidgetItem(row_data[4]))
            self.flight_list.setItem(row_idx, 5, QTableWidgetItem(row_data[5]))
            self.flight_list.setItem(row_idx, 6, QTableWidgetItem(f"${float(row_data[6]):.2f}"))
            self.flight_list.setItem(row_idx, 7, QTableWidgetItem(str(row_data[7])))
            self.flight_list.setItem(row_idx, 8, QTableWidgetItem(str(row_data[8])))

        self.flight_list.resizeColumnsToContents()

     # Display top 2 cheapest flights as offers
        if len(results) > 1:
            self.offer1_label.setText(f"Flight ID: {results[0][0]}")
            self.offer2_label.setText(f"Flight ID: {results[1][0]}")
            self.label_6.setText("")  # Clear "No offers" message
        else:
            self.offer1_label.setText("")
            self.offer2_label.setText("")
            self.label_6.setText("No offers for this flight")

    def proceed(self):

        self.master_form = Options(
            bookingID=self.booking_id
        )
        self.master_form.show()
        self.close()

# if __name__ == "__main__":
#     # Database connection string for SQL Server 2019
#     CONNECTION_STRING = (
#         "Driver={ODBC Driver 17 for SQL Server};"
#         "Server=DESKTOP-4UKQNMN\\HUSTUDENTSQL;"  # Replace with your server name
#         "Database=FlightReservationSystem;"  # Replace with your database name
#         "Trusted_Connection=yes;"
#     )
    
#     app = QtWidgets.QApplication(sys.argv)
#     window = BookingScreen(CONNECTION_STRING)
#     sys.exit(app.exec())
