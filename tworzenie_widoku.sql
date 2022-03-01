CREATE OR REPLACE VIEW traopisy AS
SELECT * FROM transakcje
INNER JOIN opisytransakcji ON Opis_transakcji = ID;

----- ten poniżej nie działa, bo jest duplikacja pola --
-- CREATE OR REPLACE VIEW allin AS
-- SELECT * FROM transakcje
-- INNER JOIN opisytransakcji T ON Opis_transakcji = T.ID
-- INNER JOIN lokalizacje L ON L.ID = T.Lokalizacja;
