/*
CREATE OR REPLACE VIEW V_HAT_GUZERGAH_SHAPE AS 
GUZERGAH_GEOLOC'UN SUTUNU SHAPE OLMUS?
 * 
 *  * 
 * 
 */

select  g.id, g.guzergah_kodu, g.guzergah_adi, h.isletme_bolgesi, h.isletme_alt_bolgesi, g.olu_km,
 case
   when g.depar_no = 0 and g.yon = 0 and g.olu_km = 0 then
    1
   else
    0
 end as ana_gidis,
 case
   when g.depar_no = 0 and g.yon = 1 and g.olu_km = 0 then
    1
   else
    0
 end as ana_donus,
 case
   when g.depar_no != 0 and g.yon = 0 and g.olu_km = 0 then
    1
   else
    0
 end as depar_gidis,
 case
   when g.depar_no != 0 and g.yon = 1 and g.olu_km = 0 then
    1
   else
    0
 end as depar_donus,  gc.SHAPE
  from guzergah g left join hat h on h.id = g.hat_id,
  (select guzergah_id, shape from guzergah_geoloc where id in (select max(id) from guzergah_geoloc group by guzergah_id)) gc
   where gc.SHAPE is not null and gc.guzergah_id = g.id
   
SELECT * FROM TESTHATYONETIM.GUZERGAH_GEOLOC gg 


SELECT MDSYS.SDO_CS.TRANSFORM(D.SHAPE , 7932, 4326) FROM V_HAT_GUZERGAH_SHAPE D