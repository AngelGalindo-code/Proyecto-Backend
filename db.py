import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="roundhouse.proxy.rlwy.net",
        user="root",
        password="FUibWHMPCpWeDRAoHRstKuBpPAuwNPPA",
        database="ProDe",
        port=31261
    )