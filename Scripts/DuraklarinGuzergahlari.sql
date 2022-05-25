--GYY .NET Reports

/*  Report 3:  Duraklarin Guzergahlari Raporu: ** View Name: VW_DURAKGUZERGAH

*/

-- POSTGRESQL: SDE-- DURAK ADI, DURAK KODU, GUZERGAH KODU, HAT KODU,-- DURAKTAN GECEN HAT SAYISI

CREATE OR REPLACE VIEW VW_DURAKGUZERGAH AS
SELECT d.durak_kisa_adi,
       d.durak_kodu,
       g.guzergah_kodu,
       g.hat_kodu,
       att.dghs as
           "DURAKTAN GECEN HAT SAYISI"
from guzergah_segment gsjoin segment s on s.globalid = gs.segment_guid
    join durak d on d.DURAK_ID = s.ba_durak_id
    join guzergah g on g.ID = gs.GUZERGAH_ID
    join (select count(g.hat_id) as dghs, g.ID, g.hat_id from guzergah_segment gs
    join segment s on s.globalid = gs.segment_guid
    join durak d on d.DURAK_ID = s.ba_durak_id
    join guzergah g on g.ID = gs.GUZERGAH_IDgroup by g.hat_id, g.ID) as att on att.hat_id = g.hat_id

