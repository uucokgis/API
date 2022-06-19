/*
SORULACAK: c.	-- GARAJDAN GARAJA: GARAJ_GARAJ_ROTA -- BAKIM ICIN VS.
YAKA BAZLI FILRELENIR,
*/

create or replace view garaj_garaj_view as

select d.durak_kodu,
       g.garaj_kodu,
       d.durak_x::numeric, d.durak_y::numeric, 
       split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 3)::numeric AS garaj_x,
       split_part(split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS garaj_y,d.isletme_bolgesi,
       g.isletme_bolgesi
from durak_coord_vw d
         join garaj g on g.garaj_kodu::text != d.durak_kodu::text 
         where d.durak_kodu in (select hatbitdurak from hatbasbitdurak_view hv) 
         and(d.isletme_bolgesi in (1,2) and g.isletme_bolgesi in (1,2)) 
         or (d.isletme_bolgesi in (3,4,5) and g.isletme_bolgesi in (3,4,5))
