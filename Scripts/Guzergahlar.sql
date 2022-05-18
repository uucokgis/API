--GYY .NET Reports 

/* 
 Report 12: 
Guzergahlar Raporu :
 ** View Name: VW_GUZERGAH
 

olu km guzergah adi,olu km guzergah kodu bos,kirilma noktalari da
bos veya 0 
7932-->4326 koordinat donusumu 
V_HAT_GUZERGAH_GEOLOC çalışmıyor bakılması gerekiyor

WORKAROUND:
V_HAT_GUZERGAH_GEOLOC tablosunda GEOLOC yerine SHAPERssutunu durdugu icin yeni bir view yaratip shapeli yaptik:
V_HAT_GUZERGAH_SHAPE

*/  



CREATE OR REPLACE VIEW VW_GUZERGAH AS SELECT g.*, MDSYS.SDO_CS.TRANSFORM(gc.GEOLOC , 7932, 4326) AS GEOLOC FROM V_GUZERGAH g 
join HAT h on h.id=g.hat_id 
join V_HAT_GUZERGAH_GEOLOC_MAP gc on gc.id=g.id