CREATE OR REPLACE VIEW VW_GILKSONDURAKLAR AS SELECT MDSYS.SDO_CS.TRANSFORM(gor.GEOLOC , 7932, 4326) AS GEOLOC,
KESIT_KODU, DURAK_KODU AS DURAK_KODU_A ,
ENVARTER_KODU AS DURAK_KODU_B, MESAFE, SURE 
FROM GUZERGAH_OLUKM_REPORT gor WHERE GUZERGAH_KODU LIKE 'O_BOS%'




/* durak--garaj tablosu 


durak durak tablosu oluşturulacak bu durak durak tablosu ba raporunun amacıyla aynı.
iki durak arasındaki mesafe ve süreyi burada tutacağız. durak kodu(a durağı) ve envanter kodu(b durağı) da buradan gelecek.
kesit kodu da guzergah kodu olacak. guzergah kodu ---> o_bos + durak a kodu + durak b kodu şeklinde olacak.

