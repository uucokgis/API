--GYY .NET Reports 

/* 
 Report 4:
 Duraklar Arasi Mesafe Suresi  Raporu:
 ** View Name: VW_DURAKSUREMESAFE


 --TESTHATYONETIM
 GUZERGAH: 54099
 GUZERGAH_GEOLOC: 41394
 GUZERGAH_GEOLOC_MAP: 4456

 --HATYONETIM
 GUZERGAH: 54939
 GUZERGAH_GEOLOC: 227066
 GUZERGAH_GEOLOC_MAP: 4456

 GUZERGAH_SEGMENT (TABLE) : GUZERGAH_GUID, SEGMENT_GUID, SIRA_NO
 SEGMENT: BA_DURAK_GUID, BI_DURAK_GUID, GLOBALID, SHAPE

 */
-- POSTGRESQL: SDE
-- BITMEK UZERE

select gs.SIRA, g.GUZERGAH_ADI, g.GUZERGAH_KODU, g.HAT_KODU, g.HAT_ID, g.SHAPE, d.DURAK_KODU,
d.DURAK_KISA_ADI, d.DURAK_ID,   -- BASLANGIC DURAK KODU, BITIS DURAK KODU YANYANA YAZMAK ICIN COZUM LAZIM
us.mesafe, us.sure
from GUZERGAH_SEGMENT gs
join SEGMENT us on us.ID = gs.SEGMENT_ID
join GUZERGAH g on g.ID = gs.GUZERGAH_ID
join DURAK d on d.DURAK_ID = us.BA_DURAK_ID or US.BI_DURAK_ID = d.DURAK_ID
WHERE gs.GUZERGAH_ID = 24401 AND gs.SEGMENT_ID = 1851;