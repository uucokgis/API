--GYY .NET Reports 

/* 
 Report 11: 
Guzergahtan bagimsiz Segmentler :
 ** View Name: VW_GDENBAGIMSIZSEGMENTLER
 
sartlar //
if _survey == null _result ="Cevap Bulunamadi"
else 
_survey = _survey.cevap == 0 ise Hayir 1 ise Evet, hiçbir sey yoksa Cevapsiz 

*/  


CREATE OR REPLACE VIEW VW_GDENBAGIMSIZSEGMENTLER AS 
SELECT ID,BA_DURAK_ADI, BA_DURAK_ID , BI_DURAK_ADI, BI_DURAK_ID, ID_A, MESAFE FROM V_SEGMENT vs 

