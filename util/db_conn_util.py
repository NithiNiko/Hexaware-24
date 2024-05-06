#from db_property_util import DBPropertyUtil
import mysql.connector as sql

class DBPropertyUtil:
    @staticmethod
    def get_parameters():
        return {
            'host': 'localhost',
            'database': 'Ecommerce',
            'user': 'root',
            'password': '123456'
        }

class DBConnectivity:
    @staticmethod
    def makeconnection():
        try:
            params = DBPropertyUtil.get_parameters()
            conn = sql.connect(
                host=params['host'],
                database=params['database'],
                user=params['user'],
                password=params['password']
            )
            return conn
        except sql.Error as e:
            print(f"Error connecting to the database: {e}")
            return None