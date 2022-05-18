--GYY .NET Reports 

/* 
 Report 14: 
 Garlar Raporu :
 ** View Name: VW_GARLAR
 
kapasite ve mevcut arac sutunlari 0 olarak geliyor.
MISTYLE ne anlama geliyor anlamadim 
7932 4326 koordinat donusumu gerceklesmistir

*/  

CREATE OR REPLACE VIEW VW_GARLAR AS SELECT ID,KULLANICI_ADI,MI_STYLE,GAR_ADI,ILCEADI,ILCE_ID,GAR_KODU,
KAPASITESI ,MEVCUT_ARAC, ISLETME_BOLGESI, ISLETME_ALT_BOLGESI,DURUMU,
MDSYS.SDO_CS.TRANSFORM(vg.GEOLOC , 7932, 4326) AS GEOLOC  
FROM V_GAR vg ORDER BY GAR_KODU 
