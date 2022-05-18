SELECT D.DURAK_KODU, D.ESKI_DURAK_ID, D.ADI, G.GUZERGAH_KODU,
D.SHAPE,(SELECT COUNT (*) FROM HAT H WHERE H.ID=G.HAT_ID) AS DURAKTAN_GECEN_HATSAYISI FROM GUZERGAH G 
JOIN SDE.GUZERGAH_SEGMENT GS ON G.ID = GS.GUZERGAH_ID 
JOIN SDE.SEGMENT S ON GS.SEGMENT_ID = S.ID 
JOIN SDE.DURAK D ON D.ESKI_DURAK_ID = S.BI_DURAK_ID WHERE S.TIP = 3 
UNION ALL 
SELECT  D.DURAK_KODU,D.ESKI_DURAK_ID,D.ADI, G.GUZERGAH_KODU, D.SHAPE,
(SELECT COUNT(*) FROM HAT H WHERE H.ID = G.HAT_ID ) AS DURAKTAN_GECEN_HATSAYISI FROM GUZERGAH G 
JOIN GUZERGAH_SEGMENT GS ON G.ID = GS.GUZERGAH_ID 
JOIN SEGMENT S ON GS.SEGMENT_ID = S.ID  
JOIN DURAK D ON D.ESKI_DURAK_ID = S.BA_DURAK_ID WHERE S.TIP = 1;


/*DURAKLARIN GUZERGAHLARI RAPORU 

DURAK ---> DURAK TABLOSU İÇİN KULLANILABİLİR. 




hat>1m guzergah> 1-1 durak


101 2 ugur 32-g0(durak-guzergah) point 25(hattan okuyacak) 
bunun sql i ilişkisel duruma göre yeniden yazılacak.



DURAK VE GUZERGAH SPATİAL JOIN İLE ÇÖZÜMLENECEK.


