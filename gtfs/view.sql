-- durak gtfs
create or replace view VW_GTFS_DURAK as
select durak_id   as stop_id,
       durak_kodu as stop_code,
       adi        as stop_name,
       aciklama   as stop_desc,
       split_part((st_astext((d.shape)::st_geometry)):: text, ' '::text, 3)::numeric AS stop_lat, split_part(split_part(
        (st_astext((d.shape)::st_geometry)):: text, ' '::text, 4), ')', 1)::numeric AS stop_lon,1 as location_type
from durak d

-- guzergah gtfs
-- --route_id*, route_short_name*, route_long_name, route_desc, route_type
create or replace view VW_GTFS_GUZERGAH as
select guzergah_id   as route_id,
       guzergah_kodu as route_short_name,
       hat_adi       as route_long_name,
       aciklama      as route_desc,
       3             as route_type
from guzergah g


