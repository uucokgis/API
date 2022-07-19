/*
 b.	-- DURAKTAN GARAJA: DURAK_GARAJ_ROTA:   Tool1: DurakGarajRoute:
YAKA BAZLI FILTRELENIR,
OK b1: tum hat sonu duraklarindan tum garajlara: HS_GARAJ_ROTA
b2: tum hat basi duraklarinin tum garajlara:  HB_GARAJ_ROTA
OK : b3: tum garajlardan tum hat basi duraklarina: GARAJ_HB_ROTA
b4: tum garajlardan tum hat sonu duraklarina: GARAJ_HS_ROTA

*/

-- 32618

-- hattin basi mi sonu mu oldugunu yazmamiz lazim

create or replace view VIEW_DURAK_GARAJ_HEPSI as select d.durak_kodu, g.garaj_kodu,  d.durak_x::numeric, d.durak_y::numeric,
split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 3)::numeric AS garaj_x,
split_part(split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS garaj_y,
d.isletme_bolgesi as d_isletme_bolgesi, g.isletme_bolgesi as g_isletme_bolgesi,
       (row_number() OVER (ORDER BY d.objectid))::integer AS row_id
from durak_coord_vw d
join garaj g on g.garaj_kodu::text != d.durak_kodu::text
where (d.durak_kodu in (select hatbasdurak from VIEW_HATBASBITDURAK hv)
or d.durak_kodu in (select hatbitdurak from view_hatbasbitdurak)) and
((d.isletme_bolgesi in (1,2) and g.isletme_bolgesi in (1,2))
   or (d.isletme_bolgesi in (3,4,5) and g.isletme_bolgesi in (3,4,5)))