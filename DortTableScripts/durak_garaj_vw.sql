create or replace view DURAK_GARAJ_VIEW as

select d.durak_kodu, g.garaj_kodu, d.isletme_bolgesi as d_isletme_bolgesi, g.isletme_bolgesi as g_isletme_bolgesi,
split_part((st_astext((d.shape)::st_geometry))::text, ' '::text, 3) AS durak_x,
split_part(split_part((st_astext((d.shape)::st_geometry))::text, ' '::text, 4), ')', 1) AS durak_y,
split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 3) AS garaj_x,
split_part(split_part((st_astext((g.geoloc)::st_geometry))::text, ' '::text, 4), ')', 1) AS garaj_y,
(row_number() OVER (ORDER BY d.objectid))::integer AS row_id
from durak d join garaj g on g.isletme_bolgesi = d.isletme_bolgesi  --290681