--GYY .NET Reports 

/* 
 Report 2: 
 Durak Anket Raporu:
 
 * UYARI
 * TODO: Burada V_DURAK icerisine gidiyor, ona henuz bakmadim ama durak ile aynidir muhtemelen
 * Kodda GroupJoin yazýyor bu ne henüz bilmiyoruz !
 * X, Y sütunlarýnda 7932'den wgs84'e koordinat dönüþümü var.
 * TODO: Cevaplar muhtemelen pivot + traverse islemleri ile filan hallediliyor
 * 
 * Sutunlar HARDCODED YAZILMIS.. :)
 * 
**/  


SELECT 

vd.ID AS DURAK_ID, vd.ADI AS DURAK_ADI,	vd.DURAK_KODU, vd.DURAK_TIPI,
vd.YON_BILGISI, ii.ILCEADI, m.ADI AS MAHALLE_ADI, 

-- Sutunlar
X	Y	C.1.1	C.1.2	C.1.3	C.1.4	
C.1.4.a	C.1.4.1	C.1.4.2	C.1.5	C.1.6	C.1.7	C.1.8	C.1.9	C.1.10	C.1.11	C.1.12	C.1.13	C.1.14	C.1.14.1	
C.1.15	C.1.16	C.1.17	C.1.17.1	C.1.17.2


-- Tablolar
FROM V_DURAK vd
INNER JOIN DURAK_ANKET_CEVAP dac ON vd.ID = dac.DURAK_ID
LEFT JOIN ILCELER ii ON ii.TUIK_ILCE_KODU = d.ILCEID
LEFT JOIN MAHALLELER ON m.TUIK_MAHALLE_KODU = d.MAHALLEID

-- Sartlar
WHERE vd.DURAK_KODU > 0