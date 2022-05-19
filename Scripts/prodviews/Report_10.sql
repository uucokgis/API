CREATE OR REPLACE VIEW VW_HAT AS SELECT h.*, MDSYS.SDO_CS.TRANSFORM(gc.GEOLOC , 7932, 4326) AS GEOLOC  FROM GUZERGAH g 
join V_HAT h on h.id=g.hat_id 
join (select * from guzergah_geoloc where id in 
(select max(id)from guzergah_geoloc group by guzergah_id)) gc on gc.guzergah_id = g.id


/* base tablolardan hat, guzergah_geoloc ve guzergah arasında çözümlenebilir.
V_HAT---HAT BASE

GUZERGAH HAT JOIN