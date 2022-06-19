/*
SORULACAK: c.	-- GARAJDAN GARAJA: GARAJ_GARAJ_ROTA -- BAKIM ICIN VS.
YAKA BAZLI FILRELENIR,
*/

create or replace view VIEW_GARAJ_GARAJ as

select g.garaj_kodu as bas_garaj_kodu, g2.garaj_kodu as bit_garaj_kodu,
(row_number() OVER (ORDER BY g.garaj_kodu))::integer AS row_id,
split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 3)::numeric AS bas_garaj_x,
split_part(split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS bas_garaj_y,
split_part((st_astext((g2.geoloc)::st_geometry))::text, ' '::text, 3)::numeric AS bit_garaj_x,
split_part(split_part((st_astext((g2.geoloc)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS bit_garaj_y
from garaj g inner join garaj g2 on g.garaj_kodu != g2.garaj_kodu
