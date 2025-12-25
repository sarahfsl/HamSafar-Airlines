import sys
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
from booking import BookingScreen


class SearchScreen(QtWidgets.QMainWindow):
    def __init__(self, booking_id,connection_string):
        super().__init__()
        uic.loadUi("search_screen.ui", self)

        self.connection_string = connection_string
        self.booking_id=booking_id

        # -------- ONE WAY WIDGETS --------
        self.from_one_way = self.findChild(QtWidgets.QComboBox, "from_one_way_combo")
        self.to_one_way = self.findChild(QtWidgets.QComboBox, "To_one_way_combo")
        self.date_one_way = self.findChild(QtWidgets.QDateEdit, "date_one_way")
        self.class_one_way = self.findChild(QtWidgets.QComboBox, "class_one_way")
        self.search_one_way_btn = self.findChild(QtWidgets.QPushButton, "search_button_one_way")

        # -------- ROUND TRIP WIDGETS --------
        self.from_round = self.findChild(QtWidgets.QComboBox, "from_round_trip_combo")
        self.to_round = self.findChild(QtWidgets.QComboBox, "To_round_trip_combo")
        self.out_date = self.findChild(QtWidgets.QDateEdit, "arrivale_date_round")
        self.return_date = self.findChild(QtWidgets.QDateEdit, "come_back_round_date")
        self.class_round = self.findChild(QtWidgets.QComboBox, "class_round_trip")
        self.search_round_btn = self.findChild(QtWidgets.QPushButton, "search_round_button")

        # Set minimum dates
        today = QDate.currentDate()
        self.date_one_way.setDate(today)
        self.date_one_way.setMinimumDate(today)
        self.out_date.setDate(today)
        self.out_date.setMinimumDate(today)
        self.return_date.setDate(today.addDays(7))
        self.return_date.setMinimumDate(today)

        # Connect buttons
        self.search_one_way_btn.clicked.connect(self.search_one_way)
        self.search_round_btn.clicked.connect(self.search_round_trip)
        

        # Validate return date
        self.out_date.dateChanged.connect(self.validate_return_date)

        # Load data
        self.load_airports()
        self.load_classes()

    # ---------------- DATABASE HELPERS ----------------
    def get_connection(self):
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to database:\n{str(e)}")
            return None

    def load_airports(self):
        query = """
        SELECT CONCAT(a.Name, ', ', c.CityName) AS AirportCity
        FROM Airport a
        JOIN Cities c ON a.CityID = c.CityID
        ORDER BY c.CityName, a.Name
        """
        conn = self.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            airports = [row[0] for row in cursor.fetchall()]
            conn.close()

            self.from_one_way.addItems(airports)
            self.to_one_way.addItems(airports)
            self.from_round.addItems(airports)
            self.to_round.addItems(airports)
            # self.from_round.setCurrentIndex(-1)
            # # self.class_round.addItems(classes)
            # self.to_round.setCurrentIndex(-1)
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load airports:\n{str(e)}")

    def load_classes(self):
        query = "SELECT ClassName FROM Class ORDER BY ClassMultiplier desc"
        conn = self.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            classes = [row[0] for row in cursor.fetchall()]
            for i in classes:
                print(i)
            conn.close()

            self.class_one_way.addItems(classes)
            self.class_round.addItems(classes)
            self.class_one_way.setCurrentIndex(-1)
            self.class_round.setCurrentIndex(-1)

        except pyodbc.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load classes:\n{str(e)}")

    def validate_return_date(self):
        if self.return_date.date() < self.out_date.date():
            self.return_date.setDate(self.out_date.date().addDays(1))

    # ---------------- SEARCH FUNCTIONS ----------------
    def search_one_way(self):
        from_city = self.from_one_way.currentText()
        to_city = self.to_one_way.currentText()
        dep_date = self.date_one_way.date().toString("yyyy-MM-dd")
        class_name = self.class_one_way.currentText()

        # Basic Validation
        if not from_city or not to_city:
            QMessageBox.warning(self, "Input Error", "Please select both cities.")
            return
        if from_city == to_city:
            QMessageBox.warning(self, "Input Error", "Departure and arrival cities must be different.")
            return

        # Check if flights exist in database
        query = """
        SELECT f.FlightID
        FROM Flight f
        JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
        JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
        JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
        JOIN Class c ON c.ClassName = ?
        WHERE CONCAT(a_dep.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_dep.CityID)) = ?
        AND CONCAT(a_arr.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_arr.CityID)) = ?
        AND fs.DepartureDate = ?
        """
        conn = self.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(query, (class_name, from_city, to_city, dep_date))
            flights = cursor.fetchall()
            conn.close()
            if not flights:
                QMessageBox.information(self, "No Flights", "No flights found for your selection.")
                return
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to search flights:\n{str(e)}")
            return

        # Open BookingScreen for one-way flight
        self.booking_screen = BookingScreen(from_city, to_city, dep_date, class_name,self.booking_id, self.connection_string)
        self.booking_screen.show()


    def search_round_trip(self):
        from_city = self.from_round.currentText()
        to_city = self.to_round.currentText()
        out_date = self.out_date.date().toString("yyyy-MM-dd")
        ret_date = self.return_date.date().toString("yyyy-MM-dd")
        class_name = self.class_round.currentText()

        # Basic Validation
        if not from_city or not to_city:
            QMessageBox.warning(self, "Input Error", "Please select both cities.")
            return
        if from_city == to_city:
            QMessageBox.warning(self, "Input Error", "Departure and arrival cities must be different.")
            return
        if self.return_date.date() <= self.out_date.date():
            QMessageBox.warning(self, "Date Error", "Return date must be after departure date.")
            return

        # Check outbound flights
        query_out = """
        SELECT f.FlightID
        FROM Flight f
        JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
        JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
        JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
        JOIN Class c ON c.ClassName = ?
        WHERE CONCAT(a_dep.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_dep.CityID)) = ?
        AND CONCAT(a_arr.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_arr.CityID)) = ?
        AND fs.DepartureDate = ?
        """
        # Check return flights
        query_ret = """
        SELECT f.FlightID
        FROM Flight f
        JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
        JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
        JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
        JOIN Class c ON c.ClassName = ?
        WHERE CONCAT(a_dep.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_dep.CityID)) = ?
        AND CONCAT(a_arr.Name, ', ', (SELECT CityName FROM Cities WHERE CityID=a_arr.CityID)) = ?
        AND fs.DepartureDate = ?
        """
        conn = self.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(query_out, (class_name, from_city, to_city, out_date))
            outbound = cursor.fetchall()
            cursor.execute(query_ret, (class_name, to_city, from_city, ret_date))
            inbound = cursor.fetchall()
            conn.close()

            if not outbound:
                QMessageBox.information(self, "No Flights", "No outbound flights found for your selection.")
                return
            if not inbound:
                QMessageBox.information(self, "No Flights", "No return flights found for your selection.")
                return
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to search flights:\n{str(e)}")
            return

        # Open BookingScreen for round-trip flight
        self.booking_screen = BookingScreen(
            from_city, to_city, out_date, class_name, self.connection_string, return_date=ret_date
        )
        self.booking_screen.show()



# ------------------- MAIN -------------------
if __name__ == "__main__":
    CONNECTION_STRING = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-4UKQNMN\\HUSTUDENTSQL"
        "Database=FlightReservationSystem;"
        "Trusted_Connection=yes;"
    )

    app = QtWidgets.QApplication(sys.argv)
    window = SearchScreen(CONNECTION_STRING)
    window.show()
    sys.exit(app.exec())
