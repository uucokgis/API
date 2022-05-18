--GYY .NET Reports 

/* 
 Report 9: 
Koordinatli sira durak listesi raporu :
 ** View Name: VW_KOORDINATLISIRADURAK
 
IsStop = x.BAS_DURAK_MI == 1,
LineCode = x.HAT_KODU != null ?
            x.HAT_KODU : null,
 RouteCode = x.GUZERGAH_KODU != null ?
             x.GUZERGAH_KODU : null,
 Id = x.BA_DURAK_ID != 0 ?
      x.BA_DURAK_ID : 0,
 StopName = x.BASLANGIC_ADI != null ?
            x.BASLANGIC_ADI : null,
 StopType = GetStopType(x.BA_DURAK_ID, stops, stopsType),
 Order = Convert.ToInt32(x.SIRA) != 0 ?
          Convert.ToInt32(x.SIRA) : 0,
 XCoord = Convert.ToDouble(GetGeoloc(true, x.BA_DURAK_ID, stops)),

 YCoord = Convert.ToDouble(GetGeoloc(false, x.BA_DURAK_ID, stops)),

 StopCode = stops.Find(y => y.ID == x.BA_DURAK_ID).DURAK_KODU != 0 ?
            stops.Find(y => y.ID == x.BA_DURAK_ID).DURAK_KODU : 0


*/  

-- SDO
CREATE OR REPLACE VIEW VW_KOORDINATLISIRADURAK AS 

SELECT HAT_KODU,GUZERGAH_KODU,BASLANGIC_ADI, MDSYS.SDO_CS.TRANSFORM(D.GEOLOC , 7932, 4326) AS GEOLOC,
d.DURAK_KODU,d.DURAK_TIPI SIRA 
FROM V_DURAK_SIRA vds 
JOIN DURAK d ON D.ID = vds.BA_DURAK_ID WHERE BAS_DURAK_MI =1;

--SDE
SELECT HAT_KODU,GUZERGAH_KODU,BASLANGIC_ADI, d.SHAPE,
d.DURAK_KODU,d.DURAK_TIPI SIRA 
FROM -V_DURAK_SIRA vds 
JOIN SDE.DURAK d ON D.ID = vds.BA_DURAK_ID WHERE BAS_DURAK_MI =1;

SELECT * FROM HATYONETIM.V_DURAK_SIRA vds 
