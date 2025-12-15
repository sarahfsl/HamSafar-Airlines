import pyodbc

# Database connection configuration
server = 'localhost\SQLSERVER1'
database = 'FlightManagementSystem'
use_windows_auth = True
username = 'sa'  # Only needed if not using Windows auth
password = '$ql123'  # Only needed if not using Windows auth

def get_connection():
    if use_windows_auth:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    else:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)
