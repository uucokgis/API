SELECT * FROM TESTHATYONETIM.PERON;

SELECT * FROM TESTHATYONETIM.PERON_H;


SELECT max(id) FROM GUZERGAH_LOG;
SELECT registration_id FROM SDE.TABLE_REGISTRY WHERE TABLE_NAME = 'GUZERGAH_LOG';
SELECT last_number FROM USER_SEQUENCES WHERE SEQUENCE_NAME = 'R3';
SELECT R3.NEXTVAL FROM dual;
SELECT last_number FROM user_sequences WHERE sequence_name = 'R3';


SELECT * FROM GUZERGAH g 

select max(id) FROM GUZERGAH g
SELECT registration_id FROM sde.TABLE_REGISTRY tr WHERE table_name = 'GUZERGAH_LOG'
SELECT last_number FROM USER_SEQUENCES WHERE sequence_name = 'R3'
SELECT R3.NEXTVAL FROM dual;

SELECT * FROM DURAK d 
SELECT * FROM GARAJ g 

SELECT * FROM GARAJ_H

SELECT COUNT(*) FROM BOLGE b 

SELECT * FROM HATYONETIM.MAHALLELER m ;

SELECT * FROM HATYONETIM.GAR g ;
SELECT * FROM HATYONETIM.GAR_ALANI ga;

ALTER USER SDE IDENTIFIED BY "Arc.21042021" ACCOUNT UNLOCK; 

UPDATE sde.durak_2 SET stop_id = objectid;
UPDATE sde.durak_2 SET stop_name = ADI;

SELECT *FROM sde.durak_2 d;
