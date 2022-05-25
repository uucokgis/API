--GYY .NET Reports

/*
 Report 12:
 Guzergahin ilk son durak raporu:
 ** View Name: VW_GUZ_ILKSON_DURAK_VW
 * XA, XB, YA, YB, KESITKODU?, DURAKKODUA, DURAKKODUB, MESAFE, SURE
 *


*/

-- POSTGRESQL: SDE
-- BITMEK UZERE
select gs.guzergah_id, d.durak_kodu as basdurakkodu,
d2.durak_kodu as bitdurakkodu, s2.ID, gs.sira
from guzergah_segment gs
join (
SELECT gs.guzergah_id, max(sira) as maxsira, min(sira) as minsira FROM guzergah_segment gs
join segment s on s.ID = gs.segment_id
group by gs.guzergah_id) as att on att.guzergah_id = gs.guzergah_id
join segment s2 on s2.ID = gs.segment_id
join durak d on d.DURAK_ID = s2.ba_durak_id
join durak d2 on d2.DURAK_ID = s2.bi_durak_id
where gs.guzergah_id = 23713 and
(gs.sira = maxsira OR gs.sira = minsira)
group by d.durak_kodu, gs.guzergah_id, d2.durak_kodu, att.maxsira, att.minsira, s2.ID, gs.sira