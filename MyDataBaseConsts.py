import getpass
import mysql


class Mydb:
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'Banking'
    USER = 'krystof'
    PASSWD = ''

    @staticmethod
    def SetPassword():
        Mydb.PASSWD = Mydb.PasswordPrompt()

    @staticmethod
    def PasswordPrompt():
        return getpass.getpass(prompt= 'Enter password to database: ')

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