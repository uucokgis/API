--GYY .NET Reports 

/* 
 Report 15: 
Garlar Raporu : 
 ** View Name: VW_HATBASIHATSONU_REPORT
 
Hatlara bagli olan duraklarin adlari, kodlari, koordinatlari ve hat basi garajlari ile hat sonu garajlarinin
bulundugu rapordur.
Rapor sutun basliklarinda DURAK KODU. DURAK ADI, ENLEM. BOYLAM, GARAJ1, GARAJ2 ile
devam edecek sekilde IDARE de tanimli bulunan garaj sayisina kadar devam edecek bilgileri yer alacak
sekilde tasarlanmalidir

*/  

SELECT DURAK_KODU, ADI AS DURAK_ADI, geom.X AS ENLEM, geom.Y AS BOYLAM FROM DURAK d 
JOIN SEGMENT s ON s.BA_DURAK_ID = d.ID
JOIN GUZERGAH_SEGMENT gs ON gs.SEGMENT_ID = s.ID 
JOIN GUZERGAH g ON g.ID = gs.GUZERGAH_ID 
JOIN HAT h ON h.ID = g.HAT_ID , TABLE(MDSYS.SDO_UTIL.GETVERTICES(d.GEOLOC)) geom   


SELECT HAT_BASI, HAT_SONU, GARAJ_ID, g.GARAJ_ADI FROM HAT h JOIN GARAJ g ON h.GARAJ_ID = g.ID 
