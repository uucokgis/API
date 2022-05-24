--GYY .NET Reports 

/* 
 Report 1: 
 Duraklar i�in engelli erisim listesi:
 ** View Name: VW_DURAKERISIMLISTESI
 
  * EK ISLEMLER: 
var _sart1 = Math.Max((Math.Min(item.StopDetail.O1, item.StopDetail.O3)), (Math.Min(item.StopDetail.O2, item.StopDetail.O4)));
var _sart2 = item.Stop.ENGELLI_RAMPA;

sart 1'de : Yani, Max (  Min(O1, O3) ve Min(O2, O4)  ) bulunur.
sart 2'de ENGELLI_RAMPA'ya bak�l�r == 1 ise engelli rampa vard�r.

_sart1 > 1.2  &&  _sart2: 1 -> uygun
bu durum saglanmiyorsa _neden doldurulur: Rapor ciktisinda uygunsuzluk nedeni s�tunu.

* UYARI
!! X, Y s�tunlar�nda 7932'den wgs84'e koordinat d�n�s�m� var.
	** Z sutunu  i�in kodda:
		var Z = yardimcirampa.FirstOrDefault(x => x.VALUE == item.StopDetail.Z);
		Z = Z == null ? "" : Z.TEXT
		Raporda ise "Var", "Yok" ve "" yaz�yor.
		
 _durum: Rapor ciktisinda ENGELLI ERISIME UYGUNLUK
Engelli rampa "" ise null yazilir: Bu muhtemelen styling i�in
X, Y sutunlarinda kodda niye Centroid() var anlamadim.

*/  


-- The Final Getsuga Tenshou
/* Python: ek islemlerden gelecekler:
 * X, Y, ENGELI ERISIME UYGUNLUK, UYGUNSUZLUK_NEDENI,
*/
-- SDO:

CREATE OR REPLACE VIEW SDE.VW_DURAKERISIMLISTESI AS SELECT d.DURAK_ID AS ESKI_DURAK_ID, d.ADI AS DURAK_ADI,
cast(ROW_NUMBER() OVER (ORDER BY d.DURAK_ID) as INTEGER) AS ROW_ID,
d.DURAK_KODU AS DURAK_KODU, d.OBJECTID,
ii.ILCEADI AS ILCE_ADI, m.ADI AS MAHALLE_ADI, dd.K, d.ENGELLI_RAMPA,
dd.O1, dd.O2, dd.O3, dd.O4,
d.YON_BILGISI, d.KALDIRIM_GENISLIGI, dd.Z,  d.SHAPE, SDE.ST_X(d.SHAPE) AS X, SDE.ST_Y(d.SHAPE) AS Y
FROM SDE.DURAK d
INNER JOIN SDE.DURAK_DETAY dd ON d.DURAK_ID = dd.DURAK_ID
LEFT JOIN SDE.ILCELER ii ON ii.TUIK_ILCE_KODU = d.ILCEID
LEFT JOIN SDE.MAHALLELER m ON m.TUIK_MAHALLE_KODU = d.MAHALLEID;