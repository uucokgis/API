CREATE OR REPLACE VIEW VW_GDENBAGIMSIZSEGMENTLER AS
SELECT ID, BA_DURAK_ADI, BA_DURAK_ID, BI_DURAK_ADI, BI_DURAK_ID, ID_A, MESAFE
FROM V_SEGMENT vs


/*
 Guzergah Durak Sıra tablosundan, aynı guzergahtaki sıralı iki durak

 */

/* BU RAPOR NE İÇİN KULLANILIYOR. ANLAŞILMADI. SÜTUNLARA GÖRE HER İKİ DURAK ARASINDA MESAFE HESAPLANMAKTA.
NEDEN GUZERGAHTAN BAGIMSIZ SEGMENTLER DENİLMEKTEDİR. BU DURAKLAR herhangi bir güzergaha bağlı olmaması gerekiyor ki 
gdenbagımsiz segmentleri tutalım ya da bu segmentler hiçbir türlü güzergaha etki etmemesi gerekmektedir.