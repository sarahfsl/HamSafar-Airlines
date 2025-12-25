# Importing essential modules
import Login
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QTableWidget,QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


countries_cities = {
    "France": ["Paris", "Marseille", "Lyon", "Nice", "Toulouse"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "United States": ["New York", "Los Angeles", "Chicago", "Miami", "San Francisco"],
    "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
    "Italy": ["Rome", "Milan", "Florence", "Naples", "Venice"],
    "Turkey": ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa"],
    "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Cancún", "Tijuana"],
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Krabi"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Liverpool", "Edinburgh"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Yokohama"],
    "Austria": ["Vienna", "Salzburg", "Graz", "Innsbruck", "Linz"],
    "Greece": ["Athens", "Thessaloniki", "Heraklion", "Patras", "Rhodes"],
    "Malaysia": ["Kuala Lumpur", "George Town", "Johor Bahru", "Kota Kinabalu", "Malacca"],
    "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"],
    "Portugal": ["Lisbon", "Porto", "Braga", "Coimbra", "Faro"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Mecca", "Medina", "Dammam"],
    "Poland": ["Warsaw", "Kraków", "Łódź", "Wrocław", "Gdańsk"],
    "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"],
    "Croatia": ["Zagreb", "Split", "Rijeka", "Dubrovnik", "Osijek"],
    "India": ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata"],
    "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hai Phong", "Nha Trang"],
    "Hungary": ["Budapest", "Debrecen", "Szeged", "Miskolc", "Pécs"],
    "Pakistan":["Karachi","Lahore","Islamabad","Multan","Quetta"],
    "UAE":["Dubai","Abu Dhabi","Sharjah","Ajman","Fujairah"]
}

Gender=["M","F"]

class SignUp_Screen(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Initialize the main window:
        - Load the UI file.
        - Populate the table with book data.
        - Fill the category dropdown (comboBox).
        - Connect buttons to their respective functions.
        """
        super(SignUp_Screen, self).__init__()
        uic.loadUi("signUP_user.ui",self)

        # self.user_btn.clicked.connect(self.user_role)
        # self.admin_btn.clicked.connect(self.admin_role)

        self.gender.addItems([c for c in Gender])

        self.gender.setCurrentIndex(-1)

        self.countryBox.addItems(list(countries_cities.keys()))

        self.countryBox.setCurrentIndex(-1)

        self.nationality.addItems(list(countries_cities.keys()))

        self.nationality.setCurrentIndex(-1)

        self.countryBox.currentTextChanged.connect(self.update_city)

        # self.start.clicked.connect(self.insert_user)

        self.signUpButton.clicked.connect(self.insert_user)

        # self.disable_form()
        
        # self.show()
    
#     def disable_form(self):
#         """Disable all form elements except User and Admin buttons"""
#         if self.id_entry:
#             self.id_entry.setEnabled(False)
#             self.id_entry.clear()
        
#         if self.pass_entry:
#             self.pass_entry.setEnabled(False)
#             self.pass_entry.clear()
        
#         if self.login_btn:
#             self.login_btn.setEnabled(False)
        
#         if self.signup_btn:
#             self.signup_btn.setEnabled(False)
        
#         # Keep User and Admin buttons enabled
#         if self.user_btn:
#             self.user_btn.setEnabled(True)

#         if self.admin_btn:
#             self.admin_btn.setEnabled(True)

#     def enable_form(self):
#         """Enable all form elements after role selection"""
#         if self.id_entry:
#             self.id_entry.setEnabled(True)
        
#         if self.pass_entry:
#             self.pass_entry.setEnabled(True)
        
#         if self.login_btn:
#             self.login_btn.setEnabled(True)
        
#         if self.signup_btn:
#             self.signup_btn.setEnabled(True)
        
#         # Set focus to identifier field
#         if self.id_entry:
#             self.id_entry.setFocus()

#     def select_user_role(self):
#         """Handle User button click"""
#         self.selected_role = 'user'
#         print("User role selected")
        
#         # Visual feedback - highlight selected button
#         if self.user_btn:
#             self.user_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
#         if self.admin_btn:
#             self.admin_btn.setStyleSheet("")  # Reset admin button style
        
#         # Enable the form
#         self.enable_form()
    
#     def select_admin_role(self):
#         """Handle Admin button click"""
#         self.selected_role = 'admin'
#         print("Admin role selected")
        
#         # Visual feedback - highlight selected button
#         if self.admin_btn:
#             self.admin_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
#         if self.user_btn:
#             self.user_btn.setStyleSheet("")  # Reset user button style
        
#         # Enable the form
#         self.enable_form()
    
    
    def insert_user(self):

        # taking inputs
                FullName = self.fullName.text() 
                newpassword = self.password1.text() #enter password
                password=self.password2.text() #confirm password


                
                gender = self.gender.currentText()
                passportnumber = self.passportNo.text()
                email = self.email.text()
                postal_address = self.postalCode.text()
                CountryName = self.countryBox.currentText()
                CityName =self.city.currentText()
                Nationality = self.nationality.currentText()
                Age = self.age.text()
                PhoneNumber = self.PhoneNo.text()

        # Replace these with your own database connection details
                # server = 'DESKTOP-4UKQNMN\\HUSTUDENTSQL'
                # database = 'FlightReservationSystem'  # Name of your Northwind database
                # use_windows_authentication = True  # Set to True to use Windows Authentication
                # username = 'your_username'  # Specify a username if not using Windows Authentication
                # password = 'your_password'  # Specify a password if not using Windows Authentication


                # Create the connection string based on the authentication method chosen
                if use_windows_authentication:
                        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
                else:
                        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

                # Establish a connection to the database
                connection = pyodbc.connect(connection_string)

                # Create a cursor to interact with the database
                cursor = connection.cursor()

        #selecting IDs of country and city
                
                cursor.execute("""Select countryID from Countries where CountryName=?""",(CountryName,))
                row=cursor.fetchone()
                # print(row)
                if not row:
                        QtWidgets.QMessageBox.warning(self, "Error", "Invalid country selected.")
                        return
                CountryID=row[0]
        
                cursor.execute("""Select cityID from Cities where CityName=?""",(CityName,))
                row=cursor.fetchone()
                if not row:
                        QtWidgets.QMessageBox.warning(self, "Error", "Invalid city selected.")
                        return
                CityID=row[0]

                if len(newpassword)<8:
                        QtWidgets.QMessageBox.warning(self, "Error", "Password must be at least 8 characters long.")
                elif newpassword!=self.password2.text():
                        print(newpassword, password)
                        QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
                elif FullName=='':
                       QtWidgets.QMessageBox.warning(self, "Error", "Enter Full Name")
                elif gender=='':
                        QtWidgets.QMessageBox.warning(self, "Error", "Select your Gender")
                elif Nationality=='':
                        QtWidgets.QMessageBox.warning(self, "Error", "Select your Nationality")
                elif len(passportnumber)<10 or not passportnumber.isdigit():
                       QtWidgets.QMessageBox.warning(self, "Error", "Enter valid Passport Number")
                elif len(email)<10 or '@' not in email:
                       QtWidgets.QMessageBox.warning(self, "Error", "Enter valid email address")
                elif len(postal_address)<5:
                       QtWidgets.QMessageBox.warning(self, "Error", "Enter valid Postal Address")
                elif Age=='' or not Age.isdigit():
                        QtWidgets.QMessageBox.warning(self, "Error", "Enter Valid Age")
                        if Age.isdigit() and 100<int(Age)<0:
                               QtWidgets.QMessageBox.warning(self, "Error", "Enter Valid Age")
                               
                elif len(PhoneNumber)<10 or not PhoneNumber.isdigit():
                       QtWidgets.QMessageBox.warning(self, "Error", "Enter valid Phone Number")
                elif self.checkBox.isChecked()==False:
                       QtWidgets.QMessageBox.warning(self, "Error", "Accept Terms and Conditions")
                else:
                        
                        sql_query = """ INSERT INTO [User]
                                ([Password], Gender, PassportNumber, Email, PostalAddress, 
                                CountryID, CityID, Nationality, Age, PhoneNumber,[Full Name]) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                                """
                        cursor.execute(sql_query, (password, gender, passportnumber, email, postal_address,
                                        CountryID, CityID, Nationality, Age, PhoneNumber,FullName))
                        connection.commit()

                        if cursor.rowcount > 0:
                                QtWidgets.QMessageBox.information(self, "Success", "User Successfully Signed Up")
                        else:
                                QtWidgets.QMessageBox.warning(self, "Error", "Insert failed")

            

                # Close the database connection
                connection.close()


    def update_city(self,country):
        self.city.clear()
        if country in countries_cities:
             self.city.addItems(countries_cities[country])
        
        self.city.setCurrentIndex(-1)

    def close(self):
                """
                Close the application window.
                """
                QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window =  SignUp_Screen()
    window.show()
    
    sys.exit(app.exec())
