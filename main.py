import sys
from PyQt6 import QtWidgets
from admin_dashboard import AdminDashboard  
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AdminDashboard()  
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
