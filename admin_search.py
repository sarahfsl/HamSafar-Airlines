
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from db import get_connection
from admin_update import AdminUpdateWindow
import re


class AdminSearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/admin_search.ui", self)  

        # Setup table columns properly
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels([
            "Schedule ID", "Flight ID", "From", "To",
            "Departure Date", "Departure Time",
            "Arrival Date", "Arrival Time", "Status"
        ])

        # Load cities into combo boxes
        self.load_cities()

        # Connect search button and auto-search triggers
        self.searchbutton.clicked.connect(self.search_flights)

        self.FlightID.returnPressed.connect(self.search_flights)
        self.scheduleID.returnPressed.connect(self.search_flights)
        self.DepartureDate.returnPressed.connect(self.search_flights)
        self.arrivalDate.returnPressed.connect(self.search_flights)

        self.FromCombo.currentTextChanged.connect(self.search_flights)
        self.ToCombo.currentTextChanged.connect(self.search_flights)
        self.checkBox_dep.stateChanged.connect(self.search_flights)
        self.checkBox_arrival.stateChanged.connect(self.search_flights)

        # Connect action buttons
        self.updateButton.clicked.connect(self.update_flight)
        self.cancelButton.clicked.connect(self.cancel_flight)
        self.backButton.clicked.connect(self.close)  

        # Show all flights 
        self.search_flights()

    def load_cities(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CityName FROM Cities ORDER BY CityName")
            cities = ["All"] + [row[0] for row in cursor.fetchall()]

            self.FromCombo.clear()
            self.ToCombo.clear()
            self.FromCombo.addItems(cities)
            self.ToCombo.addItems(cities)
            self.FromCombo.setCurrentIndex(0)
            self.ToCombo.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load cities:\n{e}")
        finally:
            conn.close()

    def search_flights(self):
        # Get raw inputs
        flight_id_text = self.FlightID.text().strip()
        schedule_id_text = self.scheduleID.text().strip()
        departure_city = self.FromCombo.currentText()
        arrival_city = self.ToCombo.currentText()

        # Date filters only if checkbox is checked
        departure_date = None
        arrival_date = None
        if self.checkBox_dep.isChecked():
            departure_date = self.DepartureDate.text().strip()
        if self.checkBox_arrival.isChecked():
            arrival_date = self.arrivalDate.text().strip()

        #  parse IDs
        flight_id = None
        if flight_id_text and flight_id_text.isdigit():
            flight_id = int(flight_id_text)

        schedule_id = None
        if schedule_id_text and schedule_id_text.isdigit():
            schedule_id = int(schedule_id_text)

        # Validate date format 
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if departure_date and not date_pattern.match(departure_date):
            QMessageBox.warning(self, "Invalid Date", "Departure Date must be YYYY-MM-DD")
            return
        if arrival_date and not date_pattern.match(arrival_date):
            QMessageBox.warning(self, "Invalid Date", "Arrival Date must be YYYY-MM-DD")
            return

        # Build query
        query = """
        SELECT 
            fs.ScheduleID,
            f.FlightID, 
            c_dep.CityName AS DepartureCity, 
            c_arr.CityName AS ArrivalCity,
            fs.DepartureDate,
            fs.DepartureTime,
            fs.ArrivalDate,
            fs.ArrivalTime,
            fs.Status
        FROM Flight f
        JOIN FlightSchedule fs ON f.FlightID = fs.FlightID
        JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
        JOIN Cities c_dep ON a_dep.CityID = c_dep.CityID
        JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
        JOIN Cities c_arr ON a_arr.CityID = c_arr.CityID
        WHERE 1=1
        """
        params = []

        if flight_id is not None:
            query += " AND f.FlightID = ?"
            params.append(flight_id)

        if schedule_id is not None:
            query += " AND fs.ScheduleID = ?"
            params.append(schedule_id)

        if departure_city != "All":
            query += " AND c_dep.CityName = ?"
            params.append(departure_city)

        if arrival_city != "All":
            query += " AND c_arr.CityName = ?"
            params.append(arrival_city)

        if departure_date:
            query += " AND fs.DepartureDate = ?"
            params.append(departure_date)

        if arrival_date:
            query += " AND fs.ArrivalDate = ?"
            params.append(arrival_date)

        query += " ORDER BY fs.DepartureDate DESC, fs.ScheduleID DESC"

        # Execute query
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()

            # Clear and populate table
            self.tableWidget.setRowCount(0)
            for row_num, row_data in enumerate(results):
                self.tableWidget.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    self.tableWidget.setItem(row_num, col_num, item)

            # Feedback
            count = len(results)
            self.statusbar.showMessage(f"Found {count} flight(s)", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
            self.tableWidget.setRowCount(0)
        finally:
            conn.close()

    def update_flight(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a flight to update.")
            return

        schedule_id_item = self.tableWidget.item(row, 0)  # ScheduleID is column 0
        if not schedule_id_item:
            QMessageBox.warning(self, "Error", "Cannot read Schedule ID.")
            return

        schedule_id = schedule_id_item.text()

        # Open update window with ScheduleID
        self.update_window = AdminUpdateWindow(schedule_id)
        self.update_window.show()

    def cancel_flight(self):
        """Cancel the selected flight schedule"""
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a flight to cancel.")
            return

        # ScheduleID is in column 0
        schedule_id_item = self.tableWidget.item(row, 0)
        # Status is in  column  8
        status_item = self.tableWidget.item(row, 8)

        if not schedule_id_item:
            QMessageBox.warning(self, "Error", "Cannot read Schedule ID from selected row.")
            return

        schedule_id = schedule_id_item.text()
        current_status = status_item.text() if status_item else ""

        # Prevent cancelling already cancelled flights
        if current_status.lower() == "cancelled":
            QMessageBox.information(self, "Already Cancelled", 
                                    f"Schedule ID {schedule_id} is already cancelled.")
            return

        # Confirmation dialog 
        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            f"Are you sure you want to cancel Schedule ID {schedule_id}?\n\n",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Default button
        )

        if reply != QMessageBox.StandardButton.Yes:
            return  # User clicked No

        # Perform the cancellation
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE FlightSchedule SET Status = 'Cancelled' WHERE ScheduleID = ?",
                (schedule_id,)
            )
            
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Not Found", f"No schedule found with ID {schedule_id}.")
                return

            conn.commit()
            QMessageBox.information(self, "Success", 
                                    f"Schedule ID {schedule_id} has been cancelled successfully.")
            self.search_flights()  # Refresh the table

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", 
                                f"Failed to cancel flight:\n{e}")
        finally:
            conn.close()

    def open_dashboard(self):
        from admin_dashboard import AdminDashboard
        self.dashboard = AdminDashboard()
        self.dashboard.show()
        self.close()