CREATE OR REPLACE VIEW VW_DURAKCEPHEOLCULERI AS SELECT d.ESKI_DURAK_ID AS DURAK_ID, d.ADI AS DURAK_ADI,
d.DURAK_KODU AS DURAK_KODU, CAST(ROW_NUMBER() OVER (ORDER BY d.ESKI_DURAK_ID) AS NUMBER(38, 0)) AS ROW_ID,
dd.O1, dd.O2, dd.O3, dd.O4, 
d.SHAPE 
FROM SDE.DURAK d 
INNER JOIN SDE.DURAK_DETAY dd ON d.ESKI_DURAK_ID = dd.DURAK_ID 

/*durak detay tablosu base katman olacak. durakların kaldırım vb. gibi kısımlara olan mesafeleri yer almaktadır.
