import sys
from SignUp import *
from search import *
from admin_dashboard import *
import re
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        super(LoginScreen, self).__init__()
        
        # Load the UI file created in Qt Designer
        uic.loadUi('login_screen.ui', self)  # Replace with your .ui file name

        self.connection_string = connection_string
        self.selected_role = None  # Track if User or Admin was selected
        
        # Connect UI elements to variables using your actual object names
        self.user_btn = self.findChild(QtWidgets.QPushButton, 'user_pushbutton')  # User button
        self.admin_btn = self.findChild(QtWidgets.QPushButton, 'admin_pushbutton')  # Admin button
        self.id_entry = self.findChild(QtWidgets.QLineEdit, 'member_ID_line_edit')  # ID/Email/Passport field
        self.pass_entry = self.findChild(QtWidgets.QLineEdit, 'password_line_edit')  # Password field
        self.login_btn = self.findChild(QtWidgets.QPushButton, 'log')  # Login button
        self.signup_btn = self.findChild(QtWidgets.QPushButton, 'signup_pushbutton')  # SignUp button
        
        # Set password field to hide characters (show dots/asterisks)
        if self.pass_entry:
            self.pass_entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        # Connect buttons to their functions BEFORE disabling
        if self.user_btn:
            self.user_btn.clicked.connect(self.select_user_role)
        if self.admin_btn:
            self.admin_btn.clicked.connect(self.select_admin_role)
        if self.login_btn:
            self.login_btn.clicked.connect(self.handle_login)
        if self.signup_btn:
            self.signup_btn.clicked.connect(self.open_signup)
        
        # Initially disable everything except User and Admin buttons
        # This must come AFTER connecting the buttons
        self.disable_form()
        
        self.show()
    
    def disable_form(self):
        """Disable all form elements except User and Admin buttons"""
        if self.id_entry:
            self.id_entry.setEnabled(False)
            self.id_entry.clear()
        
        if self.pass_entry:
            self.pass_entry.setEnabled(False)
            self.pass_entry.clear()
        
        if self.login_btn:
            self.login_btn.setEnabled(False)
        
        if self.signup_btn:
            self.signup_btn.setEnabled(False)
        
        # Keep User and Admin buttons enabled
        if self.user_btn:
            self.user_btn.setEnabled(True)
        if self.admin_btn:
            self.admin_btn.setEnabled(True)
    
    def enable_form(self):
        """Enable all form elements after role selection"""
        if self.id_entry:
            self.id_entry.setEnabled(True)
        
        if self.pass_entry:
            self.pass_entry.setEnabled(True)
        
        if self.login_btn:
            self.login_btn.setEnabled(True)
        
        # if self.signup_btn:
        #     self.signup_btn.setEnabled(True)
        
        # Set focus to identifier field
        if self.id_entry:
            self.id_entry.setFocus()
    
    def select_user_role(self):
        """Handle User button click"""
        self.selected_role = 'user'
        # print("User role selected")
        
        # Visual feedback - highlight selected button
        if self.user_btn:
            self.user_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        if self.admin_btn:
            self.admin_btn.setStyleSheet("")  # Reset admin button style
        
        # Enable the form
        # self.admin_btn.setEnabled(False)
        if self.signup_btn:
            self.signup_btn.setEnabled(True)

        self.enable_form()
    
    def select_admin_role(self):
        """Handle Admin button click"""
        self.selected_role = 'admin'
        print("Admin role selected")
        
        # Visual feedback - highlight selected button
        if self.admin_btn:
            self.admin_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        if self.user_btn:
            self.user_btn.setStyleSheet("")  # Reset user button style
        
        # Enable the form
        # self.user_btn.setEnabled(False)
        if self.signup_btn:
            self.signup_btn.setEnabled(False)
        self.enable_form()
    
    def validate_passport(self, passport):
        """
        Validate passport number - should be digits only (integers as string)
        Returns: True if valid, False otherwise
        """
        return passport.isdigit()
    
    def validate_email(self, email):
        """
        Validate email format - can contain letters, digits, and special characters
        Returns: True if valid, False otherwise
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    def validate_username(self, username):
        """
        Validate username - alphanumeric (letters and digits mixed)
        Returns: True if valid, False otherwise
        """
        return username.isalnum() or all(c.isalnum() or c == '_' for c in username)
    
    def identify_input_type(self, identifier):
        """
        Identify what type of input the user entered
        Returns: 'passport', 'email', 'username', or 'invalid'
        """
        # Check if it's a passport (all digits)
        if self.validate_passport(identifier):
            return 'passport'
        
        # Check if it's an email (contains @ and follows email pattern)
        elif '@' in identifier and self.validate_email(identifier):
            return 'email'
        
        # Check if it's a username (alphanumeric)
        elif self.validate_username(identifier):
            return 'username'
        
        else:
            return 'invalid'
    
    def handle_login(self):
        """Handle login button click with validation"""
        # Check if user selected a role first
        if not self.selected_role:
            QMessageBox.warning(self, "Role Not Selected", 
                              "Please select User or Admin before logging in.")
            return
        
        identifier = self.id_entry.text().strip()
        password = self.pass_entry.text().strip()
        
        # Validate input - check if fields are empty
        if not identifier or not password:
            QMessageBox.warning(self, "Input Required", 
                              "Please enter both identifier and password.")
            return
        
        # Identify and validate the input type based on selected role
        input_type = self.identify_input_type(identifier)
        
        # Validate input format based on role
        if self.selected_role == 'user':
            # Users can login with passport or email only
            if input_type not in ['passport', 'email']:
                QMessageBox.critical(self, "Invalid Input", 
                                   "Users must login with Passport Number (digits only) or Email.")
                return
        
        elif self.selected_role == 'admin':
            # Admins can login with username or email only
            if input_type not in ['username', 'email']:
                QMessageBox.critical(self, "Invalid Input", 
                                   "Admins must login with Username (alphanumeric) or Email.")
                return
        
        # Display what type was detected (for debugging)
        print(f"Selected role: {self.selected_role}")
        print(f"Detected input type: {input_type}")
        
        # Attempt login
        result = self.authenticate(identifier, password, input_type)
        
        if result['success']:
            # Verify that the account type matches the selected role
            if result['user_type'] != self.selected_role:
                QMessageBox.critical(self, "Login Failed", 
                                   f"This account is not a {self.selected_role} account. "
                                   f"Please select the correct role.")
                return
            
            if result['user_type'] == 'user':
                QMessageBox.information(self, "Login Successful", 
                                      f"Welcome!")
                # self.open_search_flight(result['data'])3
                print(f"User Data: {result['data']}")
                # def booking_id():
                #     return result['data']['user_id']
                # booking_id = self.create_new_booking(result['data']['user_id'])
                identifier = self.member_ID_line_edit.text().strip()
                password = self.password_line_edit.text()

                query = """
                SELECT UserID
                FROM [User]
                WHERE
                (
                    Email = ?
                    OR PhoneNumber = ?
                    OR PassportNumber = ?
                )
                AND [Password] = ?
                """

                conn = pyodbc.connect(self.connection_string)
                cursor = conn.cursor()

                cursor.execute(
                    query,
                    (identifier, identifier, identifier, password)
                )

                row = cursor.fetchone()
                conn.close()

                if not row:
                    QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid credentials")
                    return

                booking_id = row[0]  # ✅ THIS IS CORRECT
                print("Logged-in User ID:", booking_id)
                user_id=booking_id
                self.master_form = SearchScreen(
                    connection_string=self.connection_string,
                    # user_id=user_id
                    booking_id=booking_id
                    # user_data=result['data']
                )
                self.master_form.show()

                self.close()
                # self.master_form = SearchScreen(CONNECTION_STRING)
                # self.master_form.show()
                
            elif result['user_type'] == 'admin':
                QMessageBox.information(self, "Login Successful", 
                                      f"Welcome Admin!\nAdmin ID: {result['data']['admin_id']}")
                # self.open_admin_search(result['data'])
                print(f"Admin Data: {result['data']}")
                self.master_form = AdminDashboard()
                self.master_form.show()
        else:
            # This is the critical part - show error message from authenticate function
            QMessageBox.critical(self, "Login Failed", result['message'])
            print(f"Login failed: {result['message']}")  # Debug print
    
    def create_new_booking(self, user_id):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Booking (userID, bookingDate, status, totalPrice)
            OUTPUT INSERTED.bookingID
            VALUES (?, GETDATE(), 'IN_PROGRESS', 0)
        """, user_id)

        booking_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return booking_id

    def authenticate(self, identifier, password, input_type):
        """
        Authenticate user credentials and determine account type
        Args:
            identifier: passport/email/username
            password: user password
            input_type: 'passport', 'email', or 'username'
        Returns: dict with success, user_type, data, and message
        """
        conn = None
        try:
            print(f"Attempting to connect to database...")  # Debug
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            print(f"Connected! Authenticating with input_type: {input_type}")  # Debug
            
            # If input is passport (digits only), only check User table
            if input_type == 'passport':
                user_query = """
                    SELECT UserID, email, nationality, phoneNumber, countryID, cityID
                    FROM [User]
                    WHERE passportNumber = ? AND [Password] = ?
                """
                cursor.execute(user_query, (identifier, password))
                user = cursor.fetchone()
                
                if user:
                    conn.close()
                    return {
                        'success': True,
                        'user_type': 'user',
                        'data': {
                            'user_id': user.UserID,
                            'email': user.email,
                            'nationality': user.nationality,
                            'phone': user.phoneNumber,
                            'country_id': user.countryID,
                            'city_id': user.cityID
                        },
                        'message': 'User login successful'
                    }
                else:
                    # Check if passport exists but password is wrong
                    check_query = """
                        SELECT COUNT(*) as count
                        FROM [User]
                        WHERE passportNumber = ?
                    """
                    cursor.execute(check_query, (identifier,))
                    result = cursor.fetchone()
                    exists = result[0] > 0 if result else False
                    conn.close()
                    print(f"Passport exists: {exists}")  # Debug
                    
                    if exists:
                        return {
                            'success': False,
                            'user_type': None,
                            'data': None,
                            'message': 'Incorrect password. Please try again.'
                        }
                    else:
                        return {
                            'success': False,
                            'user_type': None,
                            'data': None,
                            'message': 'Account does not exist. Please sign up first.'
                        }
            
            # If input is email, check both User and Admin tables
            elif input_type == 'email':
                # Try User table first
                user_query = """
                    SELECT UserID, email, nationality, phoneNumber, countryID, cityID
                    FROM [User]
                    WHERE Email = ? AND [Password] = ?
                """
                cursor.execute(user_query, (identifier, password))
                user = cursor.fetchone()
                
                if user:
                    conn.close()
                    return {
                        'success': True,
                        'user_type': 'user',
                        'data': {
                            'user_id': user.UserID,
                            'email': user.email,
                            'nationality': user.nationality,
                            'phone': user.phoneNumber,
                            'country_id': user.countryID,
                            'city_id': user.cityID
                        },
                        'message': 'User login successful'
                    }
                
                # Try Admin table
                admin_query = """
                    SELECT AdminID, username, email, position, phoneNumber
                    FROM Admin
                    WHERE Email = ? AND [Password] = ?
                """
                cursor.execute(admin_query, (identifier, password))
                admin = cursor.fetchone()
                
                if admin:
                    conn.close()
                    return {
                        'success': True,
                        'user_type': 'admin',
                        'data': {
                            'admin_id': admin.AdminID,
                            'username': admin.username,
                            'email': admin.email,
                            'position': admin.position,
                            'phone': admin.phoneNumber
                        },
                        'message': 'Admin login successful'
                    }
                
                # Check if email exists in either table
                user_exists_query = "SELECT COUNT(*) as count FROM [User] WHERE Email = ?"
                cursor.execute(user_exists_query, (identifier,))
                result = cursor.fetchone()
                user_exists = result[0] > 0 if result else False
                
                admin_exists_query = "SELECT COUNT(*) as count FROM Admin WHERE Email = ?"
                cursor.execute(admin_exists_query, (identifier,))
                result = cursor.fetchone()
                admin_exists = result[0] > 0 if result else False
                
                conn.close()
                print(f"Email exists - User: {user_exists}, Admin: {admin_exists}")  # Debug
                
                if user_exists or admin_exists:
                    return {
                        'success': False,
                        'user_type': None,
                        'data': None,
                        'message': 'Incorrect password. Please try again.'
                    }
                else:
                    return {
                        'success': False,
                        'user_type': None,
                        'data': None,
                        'message': 'Account does not exist. Please sign up first.'
                    }
            
            # If input is username (alphanumeric), only check Admin table
            elif input_type == 'username':
                admin_query = """
                    SELECT AdminID, username, email, position, phoneNumber
                    FROM Admin
                    WHERE Username = ? AND [Password] = ?
                """
                cursor.execute(admin_query, (identifier, password))
                admin = cursor.fetchone()
                
                if admin:
                    conn.close()
                    return {
                        'success': True,
                        'user_type': 'admin',
                        'data': {
                            'admin_id': admin.AdminID,
                            'username': admin.username,
                            'email': admin.email,
                            'position': admin.position,
                            'phone': admin.phoneNumber
                        },
                        'message': 'Admin login successful'
                    }
                else:
                    # Check if username exists but password is wrong
                    check_query = """
                        SELECT COUNT(*) as count
                        FROM Admin
                        WHERE Username = ?
                    """
                    cursor.execute(check_query, (identifier,))
                    result = cursor.fetchone()
                    exists = result[0] > 0 if result else False
                    conn.close()
                    print(f"Username exists: {exists}")  # Debug
                    
                    if exists:
                        return {
                            'success': False,
                            'user_type': None,
                            'data': None,
                            'message': 'Incorrect password. Please try again.'
                        }
                    else:
                        return {
                            'success': False,
                            'user_type': None,
                            'data': None,
                            'message': 'Account does not exist. Please sign up first.'
                        }
                        
        except pyodbc.Error as e:
            if conn:
                conn.close()
            print(f"Database error: {str(e)}")  # Debug
            return {
                'success': False,
                'user_type': None,
                'data': None,
                'message': f'Database error: {str(e)}'
            }
        except Exception as e:
            if conn:
                conn.close()
            print(f"General error: {str(e)}")  # Debug
            return {
                'success': False,
                'user_type': None,
                'data': None,
                'message': f'Error: {str(e)}'
            }
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    
    def open_signup(self):
        self.master_form = SignUp_Screen()
        self.master_form.show()
    

