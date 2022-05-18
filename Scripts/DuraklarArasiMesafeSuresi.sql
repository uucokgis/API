--GYY .NET Reports 

/* 
 Report 4: 
 Duraklar Arasi Mesafe Suresi  Raporu:
 ** View Name: VW_DURAKSUREMESAFE 
 
 //foreach (var item in stops)
//{
//    _data.Select(c => { c.FirstName = item.DURAK_KODU+" - " + c.FirstName; c.LastName = item.DURAK_KODU + " - " + c.LastName; return c; }).ToList();
//}

//_data = _data.ToList();

foreach (StopDistance item in _data)
{
    //item.FirstName = stops.Find(x => x.ADI == item.FirstName).DURAK_KODU + " - " + item.FirstName;
    //item.LastName = stops.Find(x => x.ADI == item.LastName).DURAK_KODU + " - " + item.LastName;
    if (item.BaDurakId > 0 && item.BiDurakId > 0)
    {
        item.FirstName = stops.Find(x => x.ID == item.BaDurakId).DURAK_KODU + " - " + item.FirstName;
        item.LastName = stops.Find(x => x.ID == item.BiDurakId).DURAK_KODU + " - " + item.LastName;

    }

}
 
@Ugul: Iki tane geoloc geliyordu, kodunu bir review yapalim.
iki tane geoloc birbirinden farkliydi. rapor iceriginde hem bitis hem de baslangic durak koordinatlari var. O yuzden ayri ayri olmasini istedim.
*/  


CREATE OR REPLACE VIEW VW_DURAKSUREMESAFE AS 

-- Ugurcan Scratch: 
SELECT(SELECT MDSYS.SDO_CS.TRANSFORM(D.GEOLOC , 7932, 4326) FROM DURAK D WHERE D.ID = VDS.BI_DURAK_ID) AS GEOLOC,
(SELECT MDSYS.SDO_CS.TRANSFORM(D.GEOLOC , 7932, 4326) FROM DURAK D WHERE D.ID = VDS.BA_DURAK_ID) AS GEOLOC, ROUND((VDS.MESAFE) / 1000, 2) AS MESAFE,
VDS.BASLANGIC_ADI,VDS.BITIS_ADI,VDS.HAT_KODU,VDS.SIRA,VDS.SEGMENT_ID,VDS.GUZERGAH_KODU,ROUND((VDS.SURE) / 60, 2) AS SURE, 
VDS.BA_DURAK_ID,VDS.BI_DURAK_ID FROM V_DURAK_SIRA VDS WHERE BI_DURAK_ID is not null


-- Umut scratch: V_DURAK_SIRA
SELECT(SELECT MDSYS.SDO_CS.TRANSFORM(D.GEOLOC , 7932, 4326) FROM DURAK D WHERE D.ID = VDS.BI_DURAK_ID) AS GEOLOC,
ROUND((VDS.MESAFE) / 1000, 2) AS MESAFE,
VDS.BASLANGIC_ADI,VDS.BITIS_ADI,VDS.HAT_KODU,VDS.SIRA,VDS.SEGMENT_ID,VDS.GUZERGAH_KODU,ROUND((VDS.SURE) / 60, 2) AS SURE, 
VDS.BA_DURAK_ID,VDS.BI_DURAK_ID 
FROM V_DURAK_SIRA VDS WHERE BI_DURAK_ID is not NULL


-- SDE @UGUR
CREATE OR REPLACE VIEW VW_DURAKSUREMESAFE AS 
SELECT (SELECT d.SHAPE FROM DURAK d WHERE d.ESKI_DURAK_ID = V_DURAK_SIRA.BI_DURAK_ID) AS SHAPE_BI,
(SELECT d2.SHAPE FROM DURAK d2 WHERE d2.ESKI_DURAK_ID=V_DURAK_SIRA.BA_DURAK_ID) AS SHAPE_BA,
ROUND((V_DURAK_SIRA.MESAFE)/1000,2) AS MESAFE,
V_DURAK_SIRA.BASLANGIC_ADI,V_DURAK_SIRA.BITIS_ADI,V_DURAK_SIRA.HAT_KODU,V_DURAK_SIRA.SIRA,V_DURAK_SIRA.SEGMENT_ID,
       V_DURAK_SIRA.GUZERGAH_KODU,ROUND((V_DURAK_SIRA.SURE) / 60, 2) AS SURE,
V_DURAK_SIRA.BA_DURAK_ID,V_DURAK_SIRA.BI_DURAK_ID,
CAST(ROW_NUMBER() OVER (ORDER BY V_DURAK_SIRA.OBJECTID) AS NUMBER(38, 0)) AS ROW_ID FROM SDE.V_DURAK_SIRA WHERE BI_DURAK_ID IS NOT NULL






select k."HAT_KODU",k."HAT_ID",k."ISLETME_BOLGESI",k."ISLETME_ALT_BOLGESI",k."GUZERGAH_ID",k."GUZERGAH_KODU",k."SIRA",k."BA_DURAK_ID",
k."BI_DURAK_ID",k."TIP",k."MESAFE",k."SURE",k."SEGMENT_ID",k."BAS_DURAK_MI",k."BIT_DURAK_MI", rownum as id,
       case
         when BAS_DURAK_MI=0 then
          (select GARAJ_ADI from sde.GARAJ g where g.ESKI_ID = k.ba_durak_id)
         when BAS_DURAK_MI=1 then
           (select ADI from sde.DURAK d where d.ESKI_DURAK_ID = k.ba_durak_id)
       end as BASLANGIC_ADI,
       case
         when BIT_DURAK_MI=0 then
          (select GARAJ_ADI from sde.GARAJ g where g.ESKI_ID = k.bi_durak_id)
         when BIT_DURAK_MI=1 then
           (select ADI from sde.DURAK d where ESKI_DURAK_ID = k.bi_durak_id)
       end as BITIS_ADI
  from (
        select  h.hat_kodu,
        h.id as hat_id,
        h.isletme_bolgesi,
        h.isletme_alt_bolgesi,
        g.id as guzergah_id,
        g.guzergah_kodu,
                gs.sira,
                s.ba_durak_id,
                s.bi_durak_id,
                s.tip,
                s.mesafe,
                s.sure,
                s.id as segment_id,
                case when (sira=1 and tip!=1) or (tip!=1) then 1 else 0 end as BAS_DURAK_MI,
                case when (sira=1 and tip!=3) or (tip!=3) then 1 else 0 end as BIT_DURAK_MI
          from sde.hat h
         inner join sde.guzergah g
            on h.id = g.hat_id
         inner join sde.guzergah_segment gs
            on gs.guzergah_id = g.id
         inner join sde.segment s
            on s.id = gs.segment_id
        union all
        select hat_kodu,hat_id,isletme_bolgesi,isletme_alt_bolgesi,guzergah_id,guzergah_kodu, newSira, bi_durak_id, null, tip, mesafe, 
        sure,segment_id, case when tip!=3 then 1 else 0 end as BAS_DURAK_MI,null as BIT_DURAK_MI
          from (select  h.hat_kodu,
          h.id as hat_id,
        h.isletme_bolgesi,
        h.isletme_alt_bolgesi,
        g.id as guzergah_id,
                        g.guzergah_kodu,
                       gs.sira,
                       s.ba_durak_id,
                       s.bi_durak_id,
                       s.tip,
                       s.mesafe,
                       s.sure,
                        s.id as segment_id,
                       row_number() over(partition by g.guzergah_kodu order by gs.sira desc) as rnk,
                       sira + 1 as newSira
                  from sde.hat h
                 inner join sde.guzergah g
                    on h.id = g.hat_id
                 inner join sde.guzergah_segment gs
                    on gs.guzergah_id = g.id
                 inner join SDE.segment s
                    on s.id = gs.segment_id) where rnk = 1) k
 order by hat_kodu,guzergah_kodu, sira;


