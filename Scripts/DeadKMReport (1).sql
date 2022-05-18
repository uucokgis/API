/*
 * 
 * BA Raporu unutulmamali: 
 * 
 * 
 MANTIK: Hat basina yakin duraktan garaja ve hat sonuna yakin duraktan garaja olan mesafe ve sureler
 ayri bir tabloda tutulacak.
 Bu degerler rotadir kus ucusu degil, dolayisiyla kredi kullanilacak.
 
 * EK TABLO: GARAJ_DURAK_NEAR tablosu. Yaka bazli olmak uzere tum duraklardan tum garajlara olan rota hesaplanmasi gerekiyor.
 * Ayrica her garaj | durak guncellendiginde bu tablonun da guncellenmesi.
 * GARAJ_KODU, DURAK_KODU, XG, YG, XD, YD, MESAFE, SURE
 * 
 * 
 * EK TABLO: GUZERGAH_GARAJ_KESIT tablosu. Trigger da olacak. 
 * O_ILK + ENYAKINGARAJ + ILK DURAK
O_SON + SON DURAK + ENYAKINGARAJ
 KESIT_KODU: Guzergahin hat basindaki duraga en yakin garajini bul +  
 
 O_ILK | O_SON +  GARAJ_ID + ENYAKINDURAK_KODU
 
 * Ana tablo guzergah. Guzergaha spatial yakin olan garajlar bulunacak (GUZERGAH_GARAJ_YAKINLIK). Iliskiden degil.

 
Eski rapor sutunlari:
ID = (int)_result[0],					URETILECEK MI?
MESAFE = (double)_result[1],			HESAPLANACAK
SURE = (double)_result[2],				HESAPLANACAK
GUZERGAH_ID = (int)_result[3],			TABLO: GUZERGAH
HAT_KODU = (string)_result[4],			TABLO: HAT
KESIT_KODU = (string)_result[5], ??		TABLO: GUZERGAH_GARAJ_KESIT
ENVARTER_KODU = (string)_result[6], ??  TABLO: ? GARAJ KODU?
DURAK_KODU = (string)_result[7],   	TABLO: DURAK

-- O_ILK ise GARAJ ve O_SON ise DURAK nokta koordinatlari
XB = (string)_result[8],
YB = (string)_result[9],
XA = (string)_result[10],
YA = (string)_result[11],			TABLO : DURAK? 
GUZERGAH_KODU = (string)_result[12], TABLO: GUZERGAH

-- MESAFE VE SURELER KUS UCUSU MU?.. -> 
	- EVETSE BU SQL ILE YAPILAMAZ. TAMAMINI ARAC ILE YAPMAK GEREKIR. 
	- HAYIRSA SORGU ILE YAPILABILIR. BA RAPORUNDAN MI YARARLANILIYOR?
		- EVETSE SORUN YOK. HAYIRSA ST_GEOMETRY ILE HEP HESAPLAMAK DAHA MANTIKLI. DURAK YERLERI DEGISEBILIR.
	  
-- KULLANILACAK TABLOLAR YUKARIDAKI SUTUNLARIN YANINA YAZILDI. DOGRU MU? 
-- BA RAPORU / SORGUSU YAZILMALI MI?
-- GUZERGAH TABLOSUNDA OLUKMGUZERGAH ID SUTUNU VAR NIYE?
-- DURAK KODU GELDIGINE GORE HAT SONUNDAKI SON DURAK MI BULUNUYOR? -> EVETSE X VE YLER BU DURAKTAN MI GELIYOR? OYLEYSE A VE B LER HAT BASI HAT SONU MU YANI
AB RAPORUNDAN GELENLER MI?

*/

SELECT d.DURAK_KODU FROM HATYONETIM.DURAK d;
SELECT h.HAT_KODU, FROM HATYONETIM.HAT h;
SELECT g.GUZERGAH_KODU, g.ID FROM HATYONETIM.GUZERGAH g; 


SELECT HAT_KODU FROM HATYONETIM.HAT h 

SELECT * FROM HATYONETIM.GAR g 

SELECT DISTINCT(ISLETME_BOLGESI) FROM sde.DURAK d 