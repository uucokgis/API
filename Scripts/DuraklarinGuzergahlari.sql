--GYY .NET Reports

/*  Report 3:  Duraklarin Guzergahlari Raporu: ** View Name: VW_DURAKGUZERGAH

*/

-- DurakGarajAracı
-- Durak kodlarını ve buffer distance aldık. Bu durak kodlarının her birine distance
-- kadar buffer atılıp garajlarla kesistirilir.
-- durak_kodu, garaj_kodu, mesafe, sure, shape

-- POSTGRESQL: SDE-- DURAK ADI, DURAK KODU, GUZERGAH KODU, HAT KODU,-- DURAKTAN GECEN HAT SAYISI

CREATE OR REPLACE VIEW VW_DURAKGUZERGAH AS

SELECT d.durak_kisa_adi, d.durak_kodu, g.guzergah_kodu, g.hat_kodu, g.ID
-- DURAKTAN GECEN HAT SAYISI
from guzergah_segment gs
join segment s on s.globalid = gs.segment_guid
join durak d on d.DURAK_ID = s.ba_durak_id
join guzergah g on g.ID = gs.GUZERGAH_ID where g.ID = 3162

----------------------
select d.durak_kodu, s.ID as s1id, s2.ID as s2id, s.ba_durak_id, s2.bi_durak_id, gs.guzergah_id, g.ID, g.hat_id, g.hat_kodu from durak d
join segment s on s.ba_durak_id = d.ID
join segment s2 on s2.bi_durak_id = d.ID
join guzergah_segment gs on gs.segment_id = s.ID
join guzergah g on g.ID = gs.guzergah_id

-----------------
SELECT g.ID, d.durak_kisa_adi,
       d.durak_kodu,
       g.guzergah_kodu,
       g.hat_kodu,
       att.dghs as
           "DURAKTAN GECEN HAT SAYISI"
from guzergah_segment gs join segment s on s.globalid = gs.segment_guid
    join durak d on d.DURAK_ID = s.ba_durak_id
    join guzergah g on g.ID = gs.GUZERGAH_ID
    join (select count(g.hat_id) as dghs, g.ID, g.hat_id from guzergah_segment gs
    join segment s on s.globalid = gs.segment_guid
    join durak d on d.DURAK_ID = s.ba_durak_id
    join guzergah g on g.ID = gs.GUZERGAH_ID group by g.hat_id, g.ID, d.DURAK_ID) as att on att.hat_id = g.hat_id
where g.ID = 3162
