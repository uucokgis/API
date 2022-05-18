--GYY .NET Reports 

/* 
 Report 2: 
 Duraklarýn Güzergahlarý :
 
 * UYARI
 * Ben bunu GYY uygulamasindaki rapor karsiliklarinda bulamadim.
 * Asagidaki SQLi koddan cektim. Anlasilan, shape isterse sql calisiyor
 * TODO: StopRoute objesini sezerden ogrenmek lazim, kodun baska bi yerinde de gecmiyor.
 
 * 
**/  

-- Report icin SQL
SELECT * 

FROM GUZERGAH g
INNER JOIN GUZERGAH_SEGMENT gs ON g.ID = gs.GUZERGAH_ID
INNER JOIN SEGMENT s ON s.ID = gs.SEGMENT_ID

WHERE d.DURAK_KODU > 0
ORDER BY d.DURAK_KODU


-- Shape icin SQL
SELECT  D.DURAK_KODU,D.ID,D.ADI, G.GUZERGAH_KODU, D.GEOLOC, 
(SELECT COUNT (*) FROM HAT H WHERE H.ID=G.HAT_ID) AS HATSAYISI 

-- tablolar 
FROM GUZERGAH G 
JOIN GUZERGAH_SEGMENT GS ON G.ID = GS.GUZERGAH_ID 
JOIN SEGMENT S ON GS.SEGMENT_ID = S.ID 
JOIN DURAK  D ON D.ID = S.BI_DURAK_ID 

-- filtreler
WHERE S.TIP = 3 

-- Bu araya firlamis ne ise yariyor hic belli degil !?
UNION ALL SELECT  D.DURAK_KODU,D.ID,D.ADI, G.GUZERGAH_KODU, D.GEOLOC, 
(SELECT COUNT(*) FROM HAT H WHERE H.ID = G.HAT_ID ) AS HATSAYISI 
FROM GUZERGAH G 
JOIN GUZERGAH_SEGMENT GS ON G.ID = GS.GUZERGAH_ID 
JOIN SEGMENT S ON GS.SEGMENT_ID = S.ID  
JOIN DURAK D ON D.ID = S.BA_DURAK_ID 

-- filtreler
WHERE S.TIP = 1

