/*
a.	-- HS DURAKTAN HB DURAKLARA: DURAK_DURAK_ROTA:  Tool2: HatbasiHatsonuDurakRota
        BA_RAPORU: BIR HAT SONU DURAGININ DIGER TUM HAT BASI DURAKLARINA
AB RAPORU GUZERGAH OLACAGI ICIN ISTENMIYOR.

YAKA BAZLI FILTRELENIR,

--kontrol edilmeli
*/

select * from hatbasbitdurak_view hv;


create or replace view VIEW_BA_RAPOR as select att.hatbitdurak, att.hatbasdurak, att.bas_durak_x, att.bas_durak_y, att.bit_durak_x, att.bit_durak_y,
       att.db_isletme_bolgesi, att.ds_isletme_bolgesi,
       (row_number() OVER (ORDER BY att.hatbasdurak))::integer AS row_id from
(select distinct hv2.hatbitdurak, hv.hatbasdurak, hv.bas_durak_x, hv.bas_durak_y,
hv2.bit_durak_x, hv2.bit_durak_y, hv.db_isletme_bolgesi, hv2.ds_isletme_bolgesi 
from VIEW_HATBASBITDURAK hv, VIEW_HATBASBITDURAK hv2
where hv.hatbasdurak != hv2.hatbitdurak 
and hv.db_isletme_bolgesi in (1,2) and hv2.ds_isletme_bolgesi in (1,2)
or hv.db_isletme_bolgesi in (3,4,5) AND hv2.ds_isletme_bolgesi IN (3,4,5)
order by hv2.hatbitdurak) as att;