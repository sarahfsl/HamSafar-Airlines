from PyQt6 import QtWidgets, uic
import sys


from admin_add import *
from admin_search import *

class AdminDashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/admin_dashboard.ui", self)  

        # Connect buttons
        self.pushButton_3.clicked.connect(self.open_add_flight)      # Add Flight
        self.pushButton_2.clicked.connect(self.open_manage_flights)  # Manage Flights

    def open_add_flight(self):
        self.add_window = AdminAddWindow()
        self.add_window.show()

    def open_manage_flights(self):
        self.manage_window = AdminSearchWindow()
        self.manage_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec_())
