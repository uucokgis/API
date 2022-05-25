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

CREATE OR REPLACE VIEW VW_DURAKERISIMLISTESI AS 

-- POSTGRESQL: SDE
-- DURAKID, DURAK ADI. DURAK KODU, ENGELLI ERISIME
-- UYGUNLUK, UYGUNSUZLUK NEDENI, O1, O2, O3, O4. K(m), ILCE ADI, MAHALLE ADI,
-- ENGELLI RAMPASI, YON BILGISI, KALDIRIM GENISLIGI, ENLEM, BOYLAM
select d.DURAK_ID, d.durak_kisa_adi, d.durak_kodu, dd.o1, dd.o2, dd.o3, dd.o4, dd.k,i.ilceadi,
m.adi as mahalle_adi, db.kaldirim_genisligi, db.kaldirim_genisligi, 
split_part(sde.st_astext(d.shape)::TEXT, ' ', 3) as ENLEM,
split_part(sde.st_astext(d.shape)::TEXT, ' ', 4) as BOYLAM
-- engelli erisime uygunluk, uygunsuzluk nedeni,yon_bilgisi 
from durak d 
join durak_detay dd on d.GLOBALID = dd.DURAK_GUID
join ilceler i on i.tuik_ilce_kodu = d.ilceid 
join mahalleler m on m.tuik_mahalle_kodu = d.mahalleid 
join durak_bilgi db on db.durak_guid = d.globalid