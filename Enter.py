import csv
import mysql.connector
import sys
from opistransakcjientry_class import OpisTransakcjiEntity as Ote
from MyDataBaseConsts import Mydb as mdbc
from transakcjaentry_class import TransakcjaEntity as Te

mdbc.SetPassword() # podaj haslo do bazy


def parse(filename):

    with open(filename, "r") as csv_file:
        line = csv_file.readline()
        fields = line.split(',')
        pass

    fields = fields[:-4]
    fields = [x.strip('"') for x in fields]
    fields.pop()

    with open(filename, "r") as CSV_All:
        rrr = csv.DictReader(CSV_All, fieldnames=fields, restkey='Opis transakcji', dialect='unix', delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\', doublequote=True, quotechar='"')
        data = []
        next(rrr)
        for row in rrr:
            for k in row.keys():
                try:
                    row.update({k:row[k].strip('"')})
                except AttributeError:
                    # Jeśli row[k] nie jest str,
                    # wtedy dla każdego elementu wykonywany jest strip.
                    row.update({k:list(map(lambda x: x.strip('"'), row[k]))})
            data.append(row)
    return data


def pipnf(dane):
    total_gtz=0
    total_ltz=0
    for d in dane:
        if True in ['fortuna' in x.lower() for x in d['Opis transakcji']]:
            if float(d['Kwota']) < 0:
                total_ltz += float(d['Kwota'])
            else:
                total_gtz += float(d['Kwota'])
    return (total_gtz, total_ltz, total_gtz+total_ltz)


# extract transakcja part and opis_transakcji part 
# and pack this parts to one tuple.
def cTrans(dane: dict):
    ot = None  # opis transakcji list.
    values=[] # list to use in add entry to database.
    ot=dane.pop('Opis transakcji') # get opis transakcji list.
    for di in dane:
        if 'saldo' in di.lower() or 'kwota' in di.lower():
            values.append(float(dane[di]))
        else:
            values.append(dane[di]) # add value from di to list.
    # here we have to process data from transakcje
    return (tuple(values), ot) if len(values) > 1 else ((values[0],), ot)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python {} filename.csv ...".format(sys.argv[0]))
        exit(0)
    sys.argv.pop(0)
    for arg in sys.argv:
        dane = parse(arg)
        for d in dane:
            try:
                tuples = cTrans(d)
                ote = Ote(tuples[1], mdbc)
                ote.PrepareObject()
                ote.SaveToDB(tuples[0])
            except:
                continue
        