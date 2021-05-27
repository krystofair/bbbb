from lokalizacjaentry_class import LokalizacjaEntity as LE
import datetime
import time
import regex
from mysqlx import errors
from transakcjaentry_class import TransakcjaEntity as Tre

import pdb

class OpisTransakcjiEntity:

    def __init__(self, ot_list, db):
        self.db = db
        self.obj = ot_list
        self.prepare = False
        self.saved = False

    def ParseTelefon(self, x: str):
        newx = ''.join(x.split())
        if len(newx) > 12:
            raise Exception(f'Telefon number has too long length.{newx}')
        return newx

    def ParseOKP(self, x):
        pt=r'Oryginalna kwota operacji: \d+'
        v=None
        try:
            l=list(filter(None, [regex.search(pt, i) for i in self.obj]))
            if len(l) != 1:
                raise Exception('[!] More elements than one as "Oryginalna kwota operacji:..."')
            l = l[0].group()
            idx = self.obj.index(l)+1
            v = x + ',' + self.obj[idx][:-4]
            v = float(v.replace(',','.',1))
        except Exception as e:
            print(e)
        return v

    def ParseDateTime(self, x):
        dataiczas = r'(?P<rok>\d{4})-(?P<miesiac>\d{2})-(?P<dzien>\d{2}) (?P<godz>\d{2}):(?P<min>\d{2}):(?P<sek>\d{2})'
        dcc = regex.compile(dataiczas)
        mo = dcc.search(x)
        if mo:
            try:
                dc = datetime.datetime(
                    int(mo.group('rok')), int(mo.group('miesiac')), int(mo.group('dzien')),
                    int(mo.group('godz')), int(mo.group('min')), int(mo.group('sek'))
                )
            except:
                print('[!] Cos nie tak z parsowaniem znacznika czasowego')
            return dc
        else:
            print('[!] error mo is empty')
            return None

    def ParseLokalizacja(self, x):
        le = LE(LE.prL(x), self.db)
        le.ParseFuther()
        nid = le.CheckInDB()
        if nid == 0:
            nid = le.SaveToDB()
        return nid

    def ParseRachunek(self, x):
        newx = ''.join(x.split())
        if len(newx) > 26:
            raise Exception(f'[!] Account number has too long length. {newx}')
        return newx

    def PrepareObject(self):
        """ Create object from list, through using function or names of tables, which are written down in special dictionary OTF. """
        if self.prepare == True:
            return 0
        obj = {}
        pominiete_pola = []
        for item in self.obj:
            klucz=''
            wartosc = None
            for name in self.OTF:
                if name.lower() in item.lower():
                    if type(self.OTF[name][0]) is str:
                        klucz = self.OTF[name][0]
                    else:
                        klucz = self.OTF[name][0](self, name)
                    try:
                        wartosc = self.OTF[name][1](self, item.split(':', 1)[1].strip())
                    except IndexError:
                        # That error popped up, where there is no second value for OTF.
                        wartosc = item.split(':', 1)[1].strip()
                    if klucz != '':
                        obj.update({klucz : wartosc})
                    break
            else:
                pominiete_pola.append(item) if item != '' else None
        self.obj = obj
        self.prepare = True
        if len(pominiete_pola) != 0:
            print('[i] None of this fields was assign.')
            print('[i] Field show with this style: "45 PLN" is normal behaviour B)')
            print(pominiete_pola)

    def SaveToDB(self, transakcja):
        if self.saved == True:
            return 0
        if self.prepare == False:
            self.PrepareObject()
            self.prepare = True
        conn = self.db.getDBConn()
        cur = conn.cursor()
        try:
            
            ins_stmt = (
                "INSERT INTO OpisyTransakcji("+', '.join([str(k) for k in self.obj.keys()])+') '
                "VALUES (" + ','.join(['%s' for i in self.obj.keys()]) + ');'
            )
            cur.execute(ins_stmt, tuple(self.obj.values()))
            tranObj = Tre(transakcja, cur.lastrowid)
            tranObj.SaveToDB(conn)
            conn.commit()
            self.saved = True
        except errors.IntegrityError as e:
            print("[!] We got an error of integrity: {}".format(e))
        except Exception as e:
            print("[!] Another error: {}".format(e))
        finally:
            cur.close()
            conn.close()

    """ Opis transakcji fields
    " Obiekt automatyzujący przetwarzanie
    " Każda wartość dla odpowiedniego klucza zawiera krotkę,
    " w której są dwa pola, 1. pole jest napisem albo funkcja
    " drugie jest puste albo zawiera funkcję parsującą wartość z pierwszego obiektu
    """
    OTF = {
            'Nazwa nadawcy' : ('Nazwa_nadawcy',), # -> Nazwa_nadawcy
            'Rachunek odbiorcy' : ('Rachunek_odbiorcy', ParseRachunek),
            'Rachunek nadawcy' : ('Rachunek_nadawcy', ParseRachunek),
            'Nazwa odbiorcy' : ('Nazwa_odbiorcy',), #...
            'Tytuł' : ('Tytul',),
            'Referencje własne zleceniodawcy' : ('Ref_wlasne_zleceniodawcy',),
            'Numer telefonu' : ('Numer_telefonu', ParseTelefon),
            'Lokalizacja' : ('Lokalizacja', ParseLokalizacja),
            # 'Lokalizacja: Kraj:, Miasto:, Adres: ...', - new object
            'Data i czas operacji' : ('Data_i_czas_operacji', ParseDateTime), 
            'Oryginalna kwota operacji' : ('Oryginalna_kwota_operacji', ParseOKP), 
            # ' kwota z waluta (35 PLN) ', # - chodzi o to że przecinek nie zostaje escape owany.
            'Numer karty' : ('Numer_karty',),
            'Numer referencyjny' : ('Nr_referencyjny',),
            'Adres nadawcy' : ('Adres_nadawcy',),
            'Adres odbiorcy' : ('Adres_odbiorcy',),
            'Operacja' : ('Operacja',)
    }
