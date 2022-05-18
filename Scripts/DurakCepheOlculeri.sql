--GYY .NET Reports 

/* 
 Report 2: 
 Durak Cephe Ölçüleri Raporu Query:
 
 * UYARI
!! X, Y sütunlarýnda 7932'den wgs84'e koordinat dönüþümü var.
 
*/  

SELECT 
REPLACE(dd.O1, ".", ","),
REPLACE(dd.O2, ".", ","),
REPLACE(dd.O3, ".", ","),
REPLACE(dd.O4, ".", ","),
d.KALDIRIM_GENISLIGI,
d.ID AS DURAK_ID, d.ADI AS DURAK_ADI,	d.DURAK_KODU,

-- Ek islemlerden gelenler: 
X	Y -- Yine 7932 -> WEGS84 

FROM DURAK d
INNER JOIN DURAK_DETAY dd ON d.ID = dd.DURAK_ID


