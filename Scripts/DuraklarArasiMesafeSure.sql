--GYY .NET Reports   /*  Report 4: Duraklar Arasi Mesafe Suresi  Raporu: ** View Name: VW_DURAKSUREMESAFE
-- --TESTHATYONETIM GUZERGAH: 54099 GUZERGAH_GEOLOC: 41394 GUZERGAH_GEOLOC_MAP: 4456
-- --HATYONETIM GUZERGAH: 54939 GUZERGAH_GEOLOC: 227066 GUZERGAH_GEOLOC_MAP: 4456
--
-- GUZERGAH_SEGMENT (TABLE) : GUZERGAH_GUID, SEGMENT_GUID, SIRA_NO
-- SEGMENT: BA_DURAK_GUID, BI_DURAK_GUID, GLOBALID, SHAPE  HAT KODU, GÜZERGAH KODU, BAŞLANGIÇ DURAK ADI,
-- BİTİŞDURAK ADI, SIRA, MESAFE(KM), SÜRE(DK), BADIJRAKID, BİDURAKID */-- POSTGRESQL: SDE-- BITMEK UZERE

-- NOTTT: durak kısa adı sorusu soruldu:

select g.hat_kodu,
       g.guzergah_kodu,
       d.durak_kisa_adi  as bas_durak_adi,
       dd.durak_kisa_adi as bit_durak_adi,
       gs.sira,
       us.mesafe,
       us.sure,
       d.durak_id        as bas_durak_id,
       dd.durak_id       as bit_durak_id
from GUZERGAH_SEGMENT gs
         join SEGMENT us
              on us.ID = gs.SEGMENT_ID
         join GUZERGAH g
              on g.ID = gs.GUZERGAH_ID
         left join DURAK d on d.DURAK_ID = us.BA_DURAK_ID
         left join DURAK dd on dd.DURAK_ID = us.BI_DURAK_ID
WHERE gs.GUZERGAH_ID = 24401
  AND gs.SEGMENT_ID = 1851;

