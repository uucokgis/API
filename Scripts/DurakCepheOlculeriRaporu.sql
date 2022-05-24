--GYY .NET Reports 

/* 
 Report 2: 
 Duraklar Cephe Olculeri Raporu:
 ** View Name: VW_DURAKCEPHEOLCULERI

EK ISLEMLER:
 DURAK GLOBALID EKLE
 DURAK_DETAY GLOBALID EKLE
 DURAT_DETAY DURAK_GUID (FK) SUTUNU AC
 DURAK_GUID SUTUNUNA DURAK GLOBALID BAS
 DURAK - DURAK_DETAY RS KUR

 */

-- POSTGRESQL: sde
CREATE OR REPLACE VIEW VW_DURAKCEPHEOLCULERI AS
SELECT d.DURAK_ID                                               AS DURAK_ID,
       d.ADI                                                    AS DURAK_ADI,
       d.DURAK_KODU                                             AS DURAK_KODU,
       cast(ROW_NUMBER() OVER (ORDER BY d.DURAK_ID) as INTEGER) AS ROW_ID,
       dd.O1,
       dd.O2,
       dd.O3,
       dd.O4,
       d.SHAPE
FROM SDE.DURAK d
         JOIN SDE.DURAK_DETAY dd ON d.GLOBALID = dd.DURAK_GUID

