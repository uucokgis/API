CREATE OR REPLACE VIEW VW_PERONLAR AS SELECT ID,KULLANICI_ADI, ACIKLAMA,ADRES,ILCE_ADI,PERON_KODU,
PERON_ADI,ALAN_TIPI,MI_STYLE,ILCE_ID,
MDSYS.SDO_CS.TRANSFORM(vp.GEOLOC , 7932, 4326) AS GEOLOC
FROM V_PERON vp 



/* v_peron ---> base peron tablosu kullanılabilir.