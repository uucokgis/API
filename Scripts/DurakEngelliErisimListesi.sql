--GYY .NET Reports 

/* 
 Report 1: 
 Duraklar için engelli erisim listesi:
 ** View Name: VW_DURAKERISIMLISTESI
 
  * EK ISLEMLER: 
var _sart1 = Math.Max((Math.Min(item.StopDetail.O1, item.StopDetail.O3)), (Math.Min(item.StopDetail.O2, item.StopDetail.O4)));
var _sart2 = item.Stop.ENGELLI_RAMPA;

sart 1'de : Yani, Max (  Min(O1, O3) ve Min(O2, O4)  ) bulunur.
sart 2'de ENGELLI_RAMPA'ya bakýlýr == 1 ise engelli rampa vardýr.

_sart1 > 1.2  &&  _sart2: 1 -> uygun
bu durum saglanmiyorsa _neden doldurulur: Rapor ciktisinda uygunsuzluk nedeni sütunu.

* UYARI
!! X, Y sütunlarýnda 7932'den wgs84'e koordinat dönüsümü var.
	** Z sutunu  için kodda:
		var Z = yardimcirampa.FirstOrDefault(x => x.VALUE == item.StopDetail.Z);
		Z = Z == null ? "" : Z.TEXT
		Raporda ise "Var", "Yok" ve "" yazýyor.
		
 _durum: Rapor ciktisinda ENGELLI ERISIME UYGUNLUK
Engelli rampa "" ise null yazilir: Bu muhtemelen styling için
X, Y sutunlarinda kodda niye Centroid() var anlamadim.

*/  


-- The Final Getsuga Tenshou
/* Python: ek islemlerden gelecekler:
 * X, Y, ENGELI ERISIME UYGUNLUK, UYGUNSUZLUK_NEDENI,
*/
-- SDO:
CREATE OR REPLACE VIEW VW_DURAKERISIMLISTESI AS SELECT d.ID AS DURAK_ID, d.ADI AS DURAK_ADI,	
d.DURAK_KODU AS DURAK_KODU, CAST(ROW_NUMBER() OVER (ORDER BY d.ID) AS NUMBER(38, 0)) AS OBJECTID,
ii.ILCEADI AS ILCE_ADI, m.ADI AS MAHALLE_ADI, dd.K, yder.TEXT AS ENGELLI_RAMPA,
dd.O1, dd.O2, dd.O3, dd.O4, 
d.YON_BILGISI, d.KALDIRIM_GENISLIGI, dd.Z,  MDSYS.SDO_CS.TRANSFORM(d.GEOLOC, 7932, 4326) AS GEOLOC
FROM DURAK d
INNER JOIN DURAK_DETAY dd ON d.ID = dd.DURAK_ID
LEFT JOIN YRDMC_DURAK_ENGELLI_RAMPA yder ON yder.VALUE = d.ENGELLI_RAMPA
LEFT JOIN ILLER i ON i.TUIK_IL_KODU = d.ILID
LEFT JOIN ILCELER ii ON ii.TUIK_ILCE_KODU = d.ILCEID
LEFT JOIN MAHALLELER m ON m.TUIK_MAHALLE_KODU = d.MAHALLEID;


-- SDE:
CREATE OR REPLACE VIEW SDE.VW_DURAKERISIMLISTESI AS 
SELECT d.ESKI_DURAK_ID AS ESKI_DURAK_ID, d.ADI AS DURAK_ADI,
 CAST(ROW_NUMBER() OVER (ORDER BY d.OBJECTID) AS NUMBER(38, 0)) AS ROW_ID,
d.DURAK_KODU AS DURAK_KODU, d.OBJECTID,
ii.ILCEADI AS ILCE_ADI, m.ADI AS MAHALLE_ADI, dd.K, d.ENGELLI_RAMPA, 
dd.O1, dd.O2, dd.O3, dd.O4, 
d.YON_BILGISI, d.KALDIRIM_GENISLIGI, dd.Z,  d.SHAPE, SDE.ST_X(d.SHAPE) AS X, SDE.ST_Y(d.SHAPE) AS Y
FROM SDE.DURAK d
INNER JOIN SDE.DURAK_DETAY dd ON d.ESKI_DURAK_ID = dd.DURAK_ID
LEFT JOIN SDE.ILLER i ON i.TUIK_IL_KODU = d.ILID
LEFT JOIN SDE.ILCELER ii ON ii.TUIK_ILCE_KODU = d.ILCEID
LEFT JOIN SDE.MAHALLELER m ON m.TUIK_MAHALLE_KODU = d.MAHALLEID;



-- Scratch
-- Get from hatyonetim and set values
SELECT * FROM SDE.DURAK_ESKIID


UPDATE SDE.DURAK d SET ESKI_DURAK_ID = (SELECT ESKI_DURAK_ID FROM SDE.DURAK_ESKIID yad WHERE yad.DURAK_KODU = d.DURAK_KODU);
UPDATE SDE.DURAK d SET MODUL_DURAK_ID2 = (SELECT TEXT FROM HATYONETIM.YRDMC_DURAK_MODUL yad WHERE yad.VALUE = d.MODUL_DURAK_ID);

SELECT MODUL_DURAK_ID2 , COUNT(*)
FROM SDE.DURAK d 
GROUP BY MODUL_DURAK_ID2
HAVING COUNT(*) > 1;
