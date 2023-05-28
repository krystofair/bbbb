from mysqlx import errors
import regex

class LokalizacjaEntity():
    def __init__(self, obj, db):
        self.obj = obj
        self.saved = False
        self.db = db
    
    def ParseFuther(self):
        if 'Adres' in self.obj:
            new_adres_value = regex.search(r'(www[.])?(?<adres>(\w*[.])*\w*[.]\w{2,3})', self.obj['Adres'])
            if new_adres_value:
                # pull only domain.
                self.obj.update(Adres=new_adres_value.group('adres'))
                self.obj.update(Kraj='INTERNET')
                self.obj.update(Miasto=None)
                
    def SaveToDB(self):
        if self.saved:
            return 0
        conn = self.db.getDBConn()
        cur = conn.cursor()
        self.ParseFuther()
        insert_stmt = (
            "INSERT INTO Lokalizacje(ID, Kraj, Miasto, Adres) "
            "VALUES (%s, %s, %s, %s);"
        )
        values = []
        for pole in ['Kraj', 'Miasto', 'Adres']:
            try:
                values.append(self.obj[pole])
            except KeyError:
                values.append('NULL')
        newid = self.GetLastIDFromDB(cur) + 1
        values.insert(0, newid)
        try:
            cur.execute(insert_stmt, tuple(values))
            conn.commit()
            self.saved = True
        except errors.IntegrityError as err:
            print(f'[!] We got an error: {err}')
        finally:
            cur.close()
            conn.close()
        return newid

    def GetLastIDFromDB(self, cur):
        query = 'SELECT ID FROM Lokalizacje ORDER BY 1 DESC LIMIT 1;'
        cur.execute(query)
        last_id = cur.fetchone()
        if not last_id:
            return 0
        else:
            return last_id[0]

    def CheckInDB(self):
        conn = self.db.getDBConn()
        cur = conn.cursor()
        self.ParseFuther()
        if not self.obj['Miasto']:
            query = f"""
                SELECT ID FROM Lokalizacje
                WHERE Kraj LIKE ('%{self.obj['Kraj']}%')
                AND Adres LIKE ('%{self.obj['Adres']}%');
            """
        else:
            query = f"""
                SELECT ID FROM Lokalizacje
                WHERE Kraj LIKE ('%{self.obj['Kraj']}%')
                AND Miasto LIKE ('%{self.obj['Miasto']}%')
                AND Adres LIKE ('%{self.obj['Adres']}%');
            """
        try:
            cur.execute(query)
            t = cur.fetchall()
            if t:
                t = t[0][0] # only ID.
            else:
                t = 0
        except errors.Error as e:
            print('[!] Some error occured.')
            print(e)
        finally:
            cur.close()
        return t

    # Process Location String :D
    # This return object Location to database
    @staticmethod
    def prL(x: str) -> dict:
        lok = {}
        # wywal etykiete lokalizacji
        xx = x.strip()
        if 'Lokalizacja:' in x:
            xx = x[x.find(': ')+2:]
        end = False
        while not end:
            # wyciagnij nazwe pola
            a = xx.find(': ')
            pole = xx[:a]
            xx = xx[a+2:] # skroc napis o wyciagniete pole
            # wyciagnij wartosc
            b = xx.find(': ')
            if b == -1: # sprawdz czy będzie nowe pole.
                b = len(xx)
                end = True # Nie -> koniec
            else:
                b = xx[:b].rfind(' ') # Tak -> kontynuuj
            wartosc = xx[:b]
            lok.update({pole : wartosc})
            xx = xx[b+1:]
        return lok