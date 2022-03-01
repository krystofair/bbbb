import getpass
import mysql


class Mydb:
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'banking'
    USER = 'root'
    PASSWD = ''

    @staticmethod
    def SetPassword():
        Mydb.PASSWD = Mydb.PasswordPrompt()

    @staticmethod
    def PasswordPrompt():
        return getpass.getpass(prompt= f'Enter password to database for user {Mydb.USER}: ')

    @staticmethod
    def getDBConn():
        conn = mysql.connector.connect(
            host = Mydb.HOST,
            port = Mydb.PORT,
            database = Mydb.DATABASE,
            user = Mydb.USER,
            password = Mydb.PASSWD
        )
        return conn
