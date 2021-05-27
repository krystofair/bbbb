# Przykładowy obiekt z parsowania.
```json
{
    'Data operacji': '2021-04-01',
    'Data waluty': '2021-03-31',
    'Typ transakcji': 'Płatność web - kod mobilny',
    'Kwota': (float),
    'waluta': (char[3]),
    'saldo-po-transakcji': (float) with sign | (string),
    'opis transakcji' : [
        'Nazwa nadawcy' (optional),
        'Rachunek odbiorcy'(optional),
        'Nazwa odbiorcy'(optional),
        'Tytuł'(optional),
        'Referencje własne zleceniodawcy'(optional),
        'Numer telefonu',
        'Lokalizacja: Kraj:, Miasto:, Adres: ...',
        'Data i czas operacji' (TIMESTAMP) (optional) 
        // ta oryginalna kwota jeszcze nie działa
        'oryginalna kwota operacji', (float), ' kwota z waluta (35 PLN) ', - chodzi o to że przecinek nie zostaje escape'owany.
        'numer karty' (zagwiazdkowana czesc),
        'numer referencyjny' (bigint), '' 
    ]
}
```
