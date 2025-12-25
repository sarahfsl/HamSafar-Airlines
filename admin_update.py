
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from db import get_connection
import re

class AdminUpdateWindow(QtWidgets.QMainWindow):
    def __init__(self, schedule_id=None):  # Accepts the ID from the search screen
        super().__init__()
        uic.loadUi("ui/admin_update.ui", self)  

        self.schedule_id = schedule_id

    # Load combos 
        self.load_cities()          
        self.load_aircrafts()
        self.load_airports()
        self.load_status_options()

        #  load flight data 
        if self.schedule_id:
            self.load_flight_data(self.schedule_id)

        # Buttons
        self.updateButton.clicked.connect(self.save_updates)
        self.backButton.clicked.connect(self.close)

    def load_cities(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CityName FROM Cities ORDER BY CityName")
            cities = [row[0] for row in cursor.fetchall()]

            self.fromCombo.clear()
            self.toCombo.clear()
            self.fromCombo.addItems(cities)
            self.toCombo.addItems(cities)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load cities:\n{e}")
        finally:
            conn.close()

    def load_aircrafts(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT AircraftID, AircraftName FROM Aircraft ORDER BY AircraftID")
            self.aircraftCombo.clear()
            for aid, name in cursor.fetchall():
                self.aircraftCombo.addItem(name, aid)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load aircraft:\n{e}")
        finally:
            conn.close()

    def load_airports(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT a.AirportID, c.CityName, a.Name, a.Code
                FROM Airport a
                JOIN Cities c ON a.CityID = c.CityID
                ORDER BY c.CityName, a.Name
            """)
            airports = cursor.fetchall()

            self.depAirportCombo.clear()
            self.ArrivalAirportCombo.clear()

            for airport_id, city, name, code in airports:
                display = f"{city} - {name} ({code})"
                self.depAirportCombo.addItem(display, airport_id)
                self.ArrivalAirportCombo.addItem(display, airport_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load airports:\n{e}")
        finally:
            conn.close()

    def load_status_options(self):
        statuses = ["scheduled", "delayed", "cancelled", "ongoing"]
        self.statusCombo.clear()
        self.statusCombo.addItems(statuses)

    def load_flight_data(self, schedule_id):
        """Load selected flight's data into all widgets, including From/To cities"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    f.FlightNumber,
                    f.BaseFare,
                    f.AircraftID,
                    f.DepartureAirportID,
                    f.ArrivalAirportID,
                    fs.DepartureDate,
                    fs.DepartureTime,
                    fs.ArrivalDate,
                    fs.ArrivalTime,
                    fs.Status,
                    c_dep.CityName AS FromCity,
                    c_arr.CityName AS ToCity
                FROM FlightSchedule fs
                JOIN Flight f ON fs.FlightID = f.FlightID
                JOIN Airport a_dep ON f.DepartureAirportID = a_dep.AirportID
                JOIN Cities c_dep ON a_dep.CityID = c_dep.CityID
                JOIN Airport a_arr ON f.ArrivalAirportID = a_arr.AirportID
                JOIN Cities c_arr ON a_arr.CityID = c_arr.CityID
                WHERE fs.ScheduleID = ?
            """, (schedule_id,))

            row = cursor.fetchone()
            if not row:
                QMessageBox.warning(self, "Not Found", "Flight schedule not found.")
                self.close()
                return

            (flight_num, base_fare, aircraft_id,
            dep_airport_id, arr_airport_id,
            dep_date, dep_time, arr_date, arr_time, status,
            from_city, to_city) = row

            #  Fill all fields
            self.flightNum.setText(flight_num)
            self.basefare.setText(str(base_fare))

            self.depDate.setText(str(dep_date))
            self.ArrivalDate.setText(str(arr_date))
            self.deptime.setText(str(dep_time))
            self.Arrivaltime.setText(str(arr_time))

            self.statusCombo.setCurrentText(status)

            # Set aircraft and airports
            self.aircraftCombo.setCurrentIndex(self.aircraftCombo.findData(aircraft_id))
            self.depAirportCombo.setCurrentIndex(self.depAirportCombo.findData(dep_airport_id))
            self.ArrivalAirportCombo.setCurrentIndex(self.ArrivalAirportCombo.findData(arr_airport_id))

            #  From and To city combos 
            self.fromCombo.setCurrentText(from_city)
            self.toCombo.setCurrentText(to_city)

            #  From/To are read-only 
            self.fromCombo.setEnabled(False)
            self.toCombo.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data:\n{e}")
            self.close()
        finally:
            conn.close()


    def save_updates(self):
        """Save changes back to database with logging and duration recalc"""
        if not self.schedule_id:
            return

        try:
            # === Get and validate inputs ===
            flight_number = self.flightNum.text().strip()
            if not flight_number:
                QMessageBox.warning(self, "Required", "Flight Number is required.")
                return

            try:
                base_fare = float(self.basefare.text().strip())
                if base_fare <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Invalid", "Base Fare must be a positive number.")
                return

            aircraft_id = self.aircraftCombo.currentData()
            dep_airport_id = self.depAirportCombo.currentData()
            arr_airport_id = self.ArrivalAirportCombo.currentData()

            if not aircraft_id or not dep_airport_id or not arr_airport_id:
                QMessageBox.warning(self, "Required", "Please select aircraft and airports.")
                return

            if dep_airport_id == arr_airport_id:
                QMessageBox.warning(self, "Invalid", "Departure and arrival airports cannot be the same.")
                return

            # Date & Time
            dep_date = self.depDate.text().strip()
            arr_date = self.ArrivalDate.text().strip()
            dep_time = self.deptime.text().strip()
            arr_time = self.Arrivaltime.text().strip()

            if not all([dep_date, arr_date, dep_time, arr_time]):
                QMessageBox.warning(self, "Required", "All date and time fields are required.")
                return

            # Validate formats
            import re
            date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            time_pattern = re.compile(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")

            if not date_pattern.match(dep_date) or not date_pattern.match(arr_date):
                QMessageBox.warning(self, "Invalid Format", "Dates must be YYYY-MM-DD.")
                return
            if not time_pattern.match(dep_time) or not time_pattern.match(arr_time):
                QMessageBox.warning(self, "Invalid Time", "Times must be HH:MM (e.g., 14:30).")
                return

            # === Check arrival after departure + calculate duration ===
            from datetime import datetime

            dep_dt_str = f"{dep_date} {dep_time}"
            arr_dt_str = f"{arr_date} {arr_time}"

            try:
                dep_dt = datetime.strptime(dep_dt_str, "%Y-%m-%d %H:%M")
                arr_dt = datetime.strptime(arr_dt_str, "%Y-%m-%d %H:%M")

                if arr_dt <= dep_dt:
                    QMessageBox.warning(self, "Invalid Schedule",
                                        "Arrival date & time must be AFTER departure.")
                    return

                duration_minutes = int((arr_dt - dep_dt).total_seconds() / 60)

            except ValueError:
                QMessageBox.warning(self, "Invalid Date/Time", "Please check date/time format.")
                return

            new_status = self.statusCombo.currentText()

            # === Database operations ===
            conn = get_connection()
            cursor = conn.cursor()

            try:
                # Get old status for logging
                cursor.execute("SELECT Status FROM FlightSchedule WHERE ScheduleID = ?", (self.schedule_id,))
                old_status_row = cursor.fetchone()
                if not old_status_row:
                    QMessageBox.warning(self, "Error", "Schedule not found.")
                    return
                old_status = old_status_row[0]

                # Update Flight table
                cursor.execute("""
                    UPDATE Flight SET
                        FlightNumber = ?, BaseFare = ?, AircraftID = ?,
                        DepartureAirportID = ?, ArrivalAirportID = ?
                    WHERE FlightID = (SELECT FlightID FROM FlightSchedule WHERE ScheduleID = ?)
                """, (flight_number, base_fare, aircraft_id, dep_airport_id, arr_airport_id, self.schedule_id))

                # Update FlightSchedule with new times, duration, and status
                cursor.execute("""
                    UPDATE FlightSchedule SET
                        DepartureDate = ?, DepartureTime = ?,
                        ArrivalDate = ?, ArrivalTime = ?,
                        Duration = ?, Status = ?
                    WHERE ScheduleID = ?
                """, (dep_date, dep_time, arr_date, arr_time, duration_minutes, new_status, self.schedule_id))

                # === Log status change if it changed ===
                if old_status != new_status:
                    admin_id = 1  # ← Replace with actual logged-in AdminID
                    remarks = f"Status changed from '{old_status}' to '{new_status}' via update"

                    cursor.execute("""
                        INSERT INTO FlightStatusLog 
                        (LogID, ScheduleID, AdminID, OldStatus, NewStatus, Remarks, UpdatedAt)
                        VALUES (
                            (SELECT ISNULL(MAX(LogID), 0) + 1 FROM FlightStatusLog),
                            ?, ?, ?, ?, ?, GETDATE()
                        )
                    """, (self.schedule_id, admin_id, old_status, new_status, remarks))

                conn.commit()
                QMessageBox.information(self, "Success",
                                        f"Flight updated successfully!\n"
                                        f"New duration: {duration_minutes} minutes")
                self.close()

            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Database Error", f"Update failed:\n{e}")
            finally:
                conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))