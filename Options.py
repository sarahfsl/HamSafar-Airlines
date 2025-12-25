from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
from db import get_connection
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QTableWidget,QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

seats = ["Aisle", "Middle", "Window"]
meals = ["Standard", "Vegetarian", "Halal"]

class Options(QtWidgets.QMainWindow):
    def __init__(self,bookingID):
        super().__init__()
        uic.loadUi("options.ui", self)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.bookingID = bookingID

        # Populate dropdowns
        self.seat.addItems(seats)
        self.meal.addItems(meals)

        self.seat.setCurrentIndex(-1)
        self.meal.setCurrentIndex(-1)

        # Button connections
        self.confirm_btn.clicked.connect(self.insert_options)
        self.back_btn.clicked.connect(self.go_back)

        

        # Database connection
        # self.conn = pyodbc.connect(
        #     "Driver={ODBC Driver 17 for SQL Server};"
        #     "Server=DESKTOP-4UKQNMN\\HUSTUDENTSQL;"  # Replace with your server name
        #     "Database=FlightReservationSystem;"  # Replace with your database name
        #     "Trusted_Connection=yes;"
        # )
        # self.cursor = self.conn.cursor()

    # ---------------- VALIDATION ---------------- #
    def validate_inputs(self):
        if self.seat.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a seat type.")
            return False

        if self.meal.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a meal type.")
            return False

        # if self.childmeal.isChecked() and self.meal.currentText() == "Standard":
        #     QtWidgets.QMessageBox.warning(
        #         self, "Error",
        #         "Child meal cannot be selected with Standard meal."
        #     )
        #     return False

        return True

    # ---------------- DATABASE HELPERS ---------------- #
    def get_id_and_cost(self, table, name_col, value):
        # conn = get_connection()
        # cursor = conn.cursor()
        query = f"SELECT {table}ID, extraCost FROM {table} WHERE {name_col}=?"
        self.cursor.execute(query, value)
        row = self.cursor.fetchone()
        return row if row else (None, 0)

    def get_fc_option_id_cost(self, option_name):
        # conn = get_connection()
        # cursor = conn.cursor()
        query = "SELECT fcOptionID, extraCost FROM FCOption WHERE fcOptionName=?"
        self.cursor.execute(query, option_name)
        return self.cursor.fetchone()

    # ---------------- INSERT LOGIC ---------------- #
    def insert_options(self):
        # conn = get_connection()
        # cursor = conn.cursor()
        if not self.validate_inputs():
            return

        seat_name = self.seat.currentText()
        meal_name = self.meal.currentText()

        seatID, seatCost = self.get_id_and_cost("SeatType", "seatTypeName", seat_name)
        mealID, mealCost = self.get_id_and_cost("MealType", "mealTypeName", meal_name)

        total_cost = seatCost + mealCost

        # Update booking with seat & meal
        self.cursor.execute("""
            UPDATE Booking
            SET SeatTypeID=?, MealTypeID=?
            WHERE bookingID=?
        """, seatID, mealID, self.bookingID)

        # FC Options Mapping
        fc_options = {
            "Infant Bassinet": self.infant,
            "Wheelchair Assistance": self.wheelchair,
            "Extra Blanket/Pillow": self.extrablanky,
            "Child Seat": self.childmeal,
            "Extra legroom Seat": self.extralegroom
        }
        # Remove old options
        self.cursor.execute(
            "DELETE FROM BookingFCOption WHERE bookingID=?",
            self.bookingID
        )

        # total_cost = 0

        for option_name, checkbox in fc_options.items():
            if checkbox.isChecked():
                fcID, fcCost = self.get_fc_option_id_cost(option_name)

                self.cursor.execute("""
                    INSERT INTO BookingFCOption (bookingID, fcOptionID)
                    VALUES (?,?)
                """, self.bookingID, fcID)

                total_cost += fcCost


        # for option_name, checkbox in fc_options.items():
        #     if checkbox.isChecked():
        #         fcID, fcCost = self.get_fc_option_id_cost(option_name)

        #         self.cursor.execute("""
        #             INSERT INTO BookingFCOption (bookingID, fcOptionID)
        #             VALUES (?,?)
        #         """, self.bookingID, fcID)

        #         total_cost += fcCost

        # Update total price
        self.cursor.execute("""
            UPDATE Booking
            SET totalPrice = totalPrice + ?
            WHERE bookingID=?
        """, total_cost, self.bookingID)

        self.conn.commit()

        # Fetch final total
        self.cursor.execute(
            "SELECT totalPrice FROM Booking WHERE bookingID=?",
            self.bookingID
        )
        final_price = self.cursor.fetchone()[0]

        QtWidgets.QMessageBox.information(
            self,
            "Success",
            f"""
        Options saved successfully!

        Add-On Cost: {total_cost} USD
        Total Flight Cost: {final_price} USD

        You may proceed for payment.
        Have a safe flight :)
        """
        )
        QApplication.quit()

        # # Update total price
        # self.cursor.execute("""
        #     UPDATE Booking
        #     SET totalPrice = totalPrice + ?
        #     WHERE bookingID=?
        # """, total_cost, self.bookingID)

        # self.conn.commit()

        # QtWidgets.QMessageBox.information(
        #     self,
        #     "Success",
        #     f"Options saved successfully!\nTotal Add On Cost: {total_cost}. You may proceed for payment. Have a safe flight :)"
        # )
    
    # ---------------- NAVIGATION ---------------- #
    def go_back(self):
        QApplication.quit()

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window =  Options(2)
    window.show()
    
    sys.exit(app.exec())



# import Login
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtCore import QDate
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
# import sys
# import pyodbc
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtCore import Qt,QDate
# from PyQt6.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QTableWidget,QHBoxLayout
# from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

# seats=["Aisle","Middle", "Window"]

# meals=["Standard","Vegetarian","Halal"]

# class Options(QtWidgets.QMainWindow):
#     def __init__(self):
#         """
#         Initialize the main window:
#         - Load the UI file.
#         - Populate the table with book data.
#         - Fill the category dropdown (comboBox).
#         - Connect buttons to their respective functions.
#         """
#         super(Options, self).__init__()
#         uic.loadUi("options.ui",self)

#         # self.user_btn.clicked.connect(self.user_role)
#         # self.admin_btn.clicked.connect(self.admin_role)

#         self.meal.addItems([c for c in meals])

#         self.meal.setCurrentIndex(-1)

#         self.seat.addItems([s for s in seats])

#         self.countryBox.setCurrentIndex(-1)

#         # self.start.clicked.connect(self.insert_user)

#     def insert_options(self):
#         user_meal=self.meals.currentText()
#         user_seat=self.seat.currentText()

#         #taking input (will implement later)
#         SeatTypeID="""Select SeatTypeID from SeatType where SeatTypeName=input of
#         user"""
#         SeatCost="""Select extraCost from SeatType where SeatTypeName=input of
#         user"""
#         mealTypeID="""Select mealTypeID from mealType where mealTypename=input of
#         user"""
#         mealCost="""Select extraCost from mealType where mealTypename=input of
#         user"""
#         FCoptionID="""select fcOptionName from FCOption where FCOptionName=input of
#         user"""
#         FCcost="""select extraCost from FCOption where FCOptionName=input of user"""
#         sql_query = """ INSERT INTO Booking
#         ([SeatTypeID], [MealTypeID])
#         VALUES (?,?)
#         """
#         TotalAddOnCost=SeatCost+mealCost+FCcost



