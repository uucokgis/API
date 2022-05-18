
CREATE OR REPLACE VIEW VW_GUZERGAH AS 
SELECT g.*, MDSYS.SDO_CS.TRANSFORM(gc.GEOLOC , 7932, 4326) AS GEOLOC FROM V_GUZERGAH g 
join HAT h on h.id=g.hat_id 
join V_HAT_GUZERGAH_GEOLOC_MAP gc on gc.id=g.id


/* burada guzergahın shape zaten guzergah bse katmanında tutulacağı için guzerhaj