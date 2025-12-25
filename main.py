import sys
from PyQt6 import QtWidgets
from admin_dashboard import AdminDashboard  
from Login import *
# Main execution


if __name__ == "__main__":
    # Database connection string for SQL Server 2019
    CONNECTION_STRING = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-4UKQNMN\\HUSTUDENTSQL;"  # Replace with your server name
        "Database=FlightReservationSystem;"  # Replace with your database name
        "Trusted_Connection=yes;"
    )
    
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen(CONNECTION_STRING)
    sys.exit(app.exec())