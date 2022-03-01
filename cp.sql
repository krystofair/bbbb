-- loading this file by source command --
delimiter //
CREATE PROCEDURE SerwisProcedure(IN OdKiedy DATE)
BEGIN
    SELECT SUM(Kwota) FROM transakcje INNER JOIN opisytransakcji ot on ot.id = opis_transakcji left join lokalizacje L on L.ID = ot.Lokalizacja where ((L.adres LIKE('%serwis%') and typ_transakcji LIKE ('%web%')) or (typ_transakcji LIKE('%rachunek%') and nazwa_nadawcy LIKE('%SERWIS%'))) and data_operacji > OdKiedy;
END
//
delimiter ;
