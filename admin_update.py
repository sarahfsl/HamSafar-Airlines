
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

    def save_updates(self):
        """Save changes back to database"""
        if not self.schedule_id:
            return

        try:
            flight_number = self.flightNum.text().strip()
            base_fare = float(self.basefare.text().strip())

            aircraft_id = self.aircraftCombo.currentData()
            dep_airport_id = self.depAirportCombo.currentData()
            arr_airport_id = self.ArrivalAirportCombo.currentData()

            dep_date = self.depDate.text().strip()
            dep_time = self.deptime.text().strip()
            arr_date = self.ArrivalDate.text().strip()
            arr_time = self.Arrivaltime.text().strip()
            status = self.statusCombo.currentText()

            # Basic validation
            if not all([flight_number, dep_date, arr_date, dep_time, arr_time]):
                QMessageBox.warning(self, "Required", "All fields must be filled.")
                return

            conn = get_connection()
            cursor = conn.cursor()
            try:
                # Update Flight
                cursor.execute("""
                    UPDATE Flight SET
                        FlightNumber = ?, BaseFare = ?, AircraftID = ?,
                        DepartureAirportID = ?, ArrivalAirportID = ?
                    WHERE FlightID = (SELECT FlightID FROM FlightSchedule WHERE ScheduleID = ?)
                """, (flight_number, base_fare, aircraft_id, dep_airport_id, arr_airport_id, self.schedule_id))

                # Update FlightSchedule
                cursor.execute("""
                    UPDATE FlightSchedule SET
                        DepartureDate = ?, DepartureTime = ?,
                        ArrivalDate = ?, ArrivalTime = ?, Status = ?
                    WHERE ScheduleID = ?
                """, (dep_date, dep_time, arr_date, arr_time, status, self.schedule_id))

                conn.commit()
                QMessageBox.information(self, "Success", "Flight updated successfully!")
                self.close()

            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Update failed:\n{e}")
            finally:
                conn.close()

        except ValueError:
            QMessageBox.warning(self, "Invalid", "Base Fare must be a number.")

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