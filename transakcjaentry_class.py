from MyDataBaseConsts import Mydb as mdbc
from mysqlx import errors

class TransakcjaEntity:
    def __init__(self, obj: tuple, id_opisu_transakcji: int):
        obj = list(obj)
        obj.append(id_opisu_transakcji)
        self.obj = tuple(obj)
    
    def SaveToDB(self, connection):
        insert_stmt = (
            "INSERT INTO Transakcje(Data_operacji, Data_waluty, Typ_transakcji, "
            "Kwota, Waluta, Saldo_po_transakcji, Opis_transakcji) "
            "VALUES (" + ', '.join(['%s' for i in self.obj]) + ');'
        )
        cur = connection.cursor()
        li = 0
        try:
            cur.execute(insert_stmt, self.obj)
        except errors.IntegrityError:
            print('Error of integrity of data in db. Esssa')
        except Exception as ex:
            print(f"[!] We got an error: {ex}")
            raise ex # for propagation the error futher.
        finally:
            cur.close()
        return li
