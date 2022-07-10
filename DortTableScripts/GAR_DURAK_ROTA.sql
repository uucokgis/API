/*
SORULACAK: HATLARDA HB, HS VE GARAJ KODU VAR AMA GARJLA ILGILI BIR SEY YOK.
 d.	-- GARDAN DURAKLARA: GAR_DURAK_ROTA (AMA SADECE HAT BASI VEYA HAT SONU OLAN DURAKLAR)
YAKA BAZLI FILTRELENIR,        
d1: GAR_HB_ROTA
d2: HS_GAR_ROTA

*/
create or replace view VIEW_DURAK_GAR_HEPSI as

select d.durak_kodu, g.gar_kodu,  d.durak_x::numeric, d.durak_y::numeric,
split_part((st_astext(g.shape))::text, ' '::text, 3)::numeric AS gar_x,
split_part(split_part((st_astext((g.shape)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS gar_y,
d.isletme_bolgesi as d_isletme_bolgesi, g.isletme_bolgesi as g_isletme_bolgesi,
       (row_number() OVER (ORDER BY d.objectid))::integer AS row_id
from durak_coord_vw d join gar g on g.gar_kodu ::text != d.durak_kodu::text
where (d.durak_kodu in (select hatbitdurak from VIEW_HATBASBITDURAK hv) or
  d.durak_kodu in (select hatbasdurak from VIEW_HATBASBITDURAK)) and
(d.isletme_bolgesi in (1,2)
and g.isletme_bolgesi in (1,2))
or (d.isletme_bolgesi in (3,4,5)
and g.isletme_bolgesi in (3,4,5))