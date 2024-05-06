from db_conn_util import DBPropertyUtil
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