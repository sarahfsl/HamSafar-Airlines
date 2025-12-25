from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime
from db import get_connection
from datetime import datetime


class AdminAddWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/admin_add.ui", self) 

        # Populate combo boxes with data from database
        self.load_cities_to_airport_combos()
        self.load_aircrafts()
        self.load_status_options()

        # Button connections
        self.addFlightButton.clicked.connect(self.add_flight)
        self.cancelButton.clicked.connect(self.close)

        #Set current date and time as default
        current = QDateTime.currentDateTime()

    def load_cities_to_airport_combos(self):
        """Load cities into From/To combos AND full airport list into dep/arr airport combos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Load cities for simple From/To
            cursor.execute("SELECT CityName FROM Cities ORDER BY CityName")
            cities = [row[0] for row in cursor.fetchall()]

            self.fromCombo.clear()
            self.toCombo.clear()
            self.fromCombo.addItems(cities)
            self.toCombo.addItems(cities)

            # Load full airport list
            cursor.execute("""
                SELECT c.CityName, a.Name, a.Code, a.AirportID
                FROM Airport a
                JOIN Cities c ON a.CityID = c.CityID
                ORDER BY c.CityName, a.Name
            """)
            airports = cursor.fetchall()

            self.depAirportCombo.clear()
            self.ArrivalAirportCombo.clear()

            for city, name, code, airport_id in airports:
                display_text = f"{city} - {name} ({code})"
                self.depAirportCombo.addItem(display_text, airport_id)
                self.ArrivalAirportCombo.addItem(display_text, airport_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load locations:\n{e}")
        finally:
            conn.close()

    def load_aircrafts(self):
        """Load AircraftName into combo, store AircraftID as data"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT AircraftID, AircraftName FROM Aircraft ORDER BY AircraftID")
            aircrafts = cursor.fetchall()

            self.aircraftCombo.clear()
            for aircraft_id, name in aircrafts:
                self.aircraftCombo.addItem(name, aircraft_id)

            if self.aircraftCombo.count() == 0:
                self.aircraftCombo.addItem("No aircraft available")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load aircraft:\n{e}")
        finally:
            conn.close()

    def load_status_options(self):
        """Load common status values"""
        statuses = ["scheduled", "delayed", "cancelled", "ongoing"]
        self.statusCombo.clear()
        self.statusCombo.addItems(statuses)
        self.statusCombo.setCurrentText("scheduled")

    def datetime_difference(self,start_date, start_time, end_date, end_time):
        """
        Returns the difference between two date-time values
        as (days, hours, minutes)
        """

        start_dt = datetime.strptime(
            f"{start_date} {start_time}", "%Y-%m-%d %H:%M"
        )
        end_dt = datetime.strptime(
            f"{end_date} {end_time}", "%Y-%m-%d %H:%M"
        )

        if end_dt < start_dt:
            raise ValueError("End date/time must be after start date/time")

        diff = end_dt - start_dt

        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes = remainder // 60

        return int((24*days)+hours+(minutes/60))



    def add_flight(self):
        try:
            # Get inputs
            flight_number = self.flightnum.text().strip()
            if not flight_number:
                QMessageBox.warning(self, "Required", "Flight Number is required.")
                return

            aircraft_id = self.aircraftCombo.currentData()
            if not aircraft_id:
                QMessageBox.warning(self, "Required", "Please select an aircraft.")
                return

            dep_airport_id = self.depAirportCombo.currentData()
            if not dep_airport_id:
                QMessageBox.warning(self, "Required", "Please select departure airport.")
                return

            arr_airport_id = self.ArrivalAirportCombo.currentData()
            if not arr_airport_id:
                QMessageBox.warning(self, "Required", "Please select arrival airport.")
                return

            if dep_airport_id == arr_airport_id:
                QMessageBox.warning(self, "Invalid", "Departure and arrival airports cannot be the same.")
                return

            # Get date and time strings
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

            # === CALCULATE DURATION IN MINUTES ===
            from datetime import datetime

            dep_datetime_str = f"{dep_date} {dep_time}"
            arr_datetime_str = f"{arr_date} {arr_time}"

            try:
                dep_dt = datetime.strptime(dep_datetime_str, "%Y-%m-%d %H:%M")
                arr_dt = datetime.strptime(arr_datetime_str, "%Y-%m-%d %H:%M")

                if arr_dt <= dep_dt:
                    QMessageBox.warning(self, "Invalid Schedule",
                                        "Arrival date & time must be AFTER departure.")
                    return

                # Calculate duration in minutes
                duration_minutes = int((arr_dt - dep_dt).total_seconds() / 60)

            except ValueError:
                QMessageBox.warning(self, "Invalid Date/Time", "Please check your date and time entries.")
                return

            # Base fare
            base_fare_text = self.basefare.text().strip()
            try:
                base_fare = float(base_fare_text)
                if base_fare <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Invalid", "Base Fare must be a positive number.")
                return

            status = self.statusCombo.currentText()

            # === Insert into database ===
            conn = get_connection()
            cursor = conn.cursor()
            try:
                # Insert into Flight
                cursor.execute("""
                    INSERT INTO Flight 
                    (FlightNumber, AircraftID, DepartureAirportID, ArrivalAirportID, BaseFare)
                    VALUES 
                        (
                        ?, ?, ?, ?, ?
                    )
                """, (flight_number, aircraft_id, dep_airport_id, arr_airport_id, base_fare))
                # Get new FlightID
                cursor.execute("SELECT MAX(FlightID) FROM Flight")
                new_flight_id = cursor.fetchone()[0]

                # Insert into FlightSchedule with calculated duration
                cursor.execute("""
                    INSERT INTO FlightSchedule 
                    (FlightID, DepartureDate, DepartureTime, ArrivalDate, ArrivalTime, Duration, Status)
                    VALUES 
                        (
                        ?, ?, ?, ?, ?, ?,?
                    )
                """, (new_flight_id, dep_date, dep_time, arr_date, arr_time,self.datetime_difference(dep_date,dep_time,arr_date,arr_time) , status))  # Duration = 0 or calculate if you want

                # === GET THE NEW ScheduleID ===
                cursor.execute("SELECT MAX(ScheduleID) FROM FlightSchedule")
                new_schedule_id = cursor.fetchone()[0]

                # === LOG THE FLIGHT CREATION ===
                admin_id = 1  # ← Change to real logged-in admin ID later
                old_status = None  # or "New"
                new_status = status
                remarks = f"New flight '{flight_number}' created"

                cursor.execute("""
                    INSERT INTO FlightStatusLog 
                    (ScheduleID, AdminID, OldStatus, NewStatus, Remarks, UpdatedAt)
                    VALUES (
                        ?, ?, ?, ?, ?, GETDATE()
                    )
                """, (new_schedule_id, admin_id, old_status, new_status, remarks))

                conn.commit()
                QMessageBox.information(self, "Success", 
                    f"Flight {flight_number} added successfully!\n"
                    f"Schedule ID: {new_schedule_id}\n"
                    f"Duration: {duration_minutes} minutes\n"
                    f"Creation logged in status history.")
                self.close()

            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Database Error", f"Failed to add flight:\n{e}")
            finally:
                conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))