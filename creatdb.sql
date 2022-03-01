CREATE DATABASE Banking;

use Banking;

-- DATABASE od razu :V
-- Będzie łatwiej potem wyszukiwać --

CREATE TABLE Lokalizacje (
	ID INTEGER PRIMARY KEY DEFAULT 1,
	Kraj VARCHAR(255),
	Miasto VARCHAR(255),
	Adres VARCHAR(255)
);

-- wartownik tabeli Lokalizacji. -- 
INSERT INTO Lokalizacje VALUES (1, NULL, NULL, 'NIEZNANY');

CREATE TABLE OpisyTransakcji (
	ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	Lokalizacja INTEGER NOT NULL DEFAULT 1,
	Data_i_czas_operacji TIMESTAMP,
	Numer_telefonu CHAR(12),
	Tytul VARCHAR(255),
	-- okazuje sie ze dla rachunkow 26 cyfr to za malo. --
	Rachunek_nadawcy CHAR(26),
	Rachunek_odbiorcy CHAR(26),
	Nazwa_nadawcy VARCHAR(255),
	Nazwa_odbiorcy VARCHAR(255),
	Adres_nadawcy VARCHAR(255),
	Adres_odbiorcy VARCHAR(255),
	Oryginalna_kwota_operacji DECIMAL(10,2),
	Ref_wlasne_zleceniodawcy VARCHAR(255),
	Numer_karty VARCHAR(50),
	Nr_referencyjny VARCHAR(255),
	Operacja VARCHAR(255),
	CONSTRAINT FOREIGN KEY (Lokalizacja) REFERENCES Lokalizacje(ID)
);

CREATE TABLE Transakcje (
	Data_operacji DATE NOT NULL,
	Data_waluty DATE NOT NULL,
	Typ_transakcji VARCHAR(255),
	Kwota DECIMAL(10,2) NOT NULL,
	Waluta CHAR(3) NOT NULL,
	Saldo_po_transakcji DECIMAL(10,2) NOT NULL,
	Opis_transakcji INTEGER NOT NULL,
	CONSTRAINT FOREIGN KEY (Opis_transakcji) REFERENCES OpisyTransakcji(ID),
	CONSTRAINT pk_transakcja PRIMARY KEY (Data_operacji, Saldo_po_transakcji)
);




-- CREATE TABLE OpisyTransakcji (
-- 	ID INTEGER PRIMARY KEY AUTO_INCREMENT, -- id obiektu -- 
-- 	Data_i_czas_operacji TIMESTAMP UNIQUE, -- primary key bo nie da się wykonać w tym samym czasie dwóch transakcji, problem ze nie ma tego czasem w danych XD --
-- 	Lokalizacja INTEGER NOT NULL,
-- 	Numer_telefonu CHAR(12), -- zakładając +48AAABBBCCC -- 
-- 	Tytul VARCHAR(255),
-- 	Rachunek_nadawcy CHAR(26), -- powołując się na NRB --
-- 	Rachunek_odbiorcy CHAR(26), -- tak samo jak w rachunku nadawcy --
--     Nazwa_nadawcy VARCHAR(255),
-- 	Nazwa_odbiorcy VARCHAR(255),
--     -- Oryginalna_kwota_operacji DECIMAL(10,3),
--     -- Referencje_wlasne_zleceniodawcy VARCHAR(255),
--     Numer_karty VARCHAR(50),
-- 	Ref_wlasne_zleceniodawcy VARCHAR(255), -- może być razem traktowane jako nr_referencyjny. 
-- 	Nr_referencyjny VARCHAR(255), -- nie wiem nawet co to jest :kappa: --
-- 	CONSTRAINT FOREIGN KEY (Lokalizacja) REFERENCES Lokalizacje(ID)
-- );



