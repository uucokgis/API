/*
Umutun calisma kagidi
*/

-- Olay: SDO -> SDE Veri tasinmasi
-- Problem: Koordinat sistemi, missing records, migrate storage tool etc.

-- OK
GRANT ALL PRIVILEGES ON HATYONETIM.DURAK TO SDE;
CREATE TABLE SDE.DURAK AS SELECT * FROM HATYONETIM.DURAK d ;

GRANT ALL PRIVILEGES ON HATYONETIM.ILLER TO SDE;
CREATE TABLE SDE.ILLER AS SELECT * FROM HATYONETIM.ILLER d ;

GRANT ALL PRIVILEGES ON HATYONETIM.ILCELER TO SDE;
CREATE TABLE SDE.ILCELER AS SELECT * FROM HATYONETIM.ILCELER d ;

GRANT ALL PRIVILEGES ON HATYONETIM.MAHALLELER TO SDE;
CREATE TABLE SDE.MAHALLELER AS SELECT * FROM HATYONETIM.MAHALLELER d ;

GRANT ALL PRIVILEGES ON HATYONETIM.BOLGE TO SDE;
CREATE TABLE SDE.BOLGE AS SELECT * FROM HATYONETIM.BOLGE d ;

GRANT ALL PRIVILEGES ON HATYONETIM.GUZERGAH TO SDE;
CREATE TABLE SDE.GUZERGAH AS SELECT * FROM HATYONETIM.GUZERGAH d ;

GRANT ALL PRIVILEGES ON HATYONETIM.GUZERGAH_GEOLOC TO SDE;
CREATE TABLE SDE.GUZERGAH_GEOLOC AS SELECT * FROM HATYONETIM.GUZERGAH_GEOLOC d ;

GRANT ALL PRIVILEGES ON HATYONETIM.GARAJ TO SDE;
CREATE TABLE SDE.GARAJ AS SELECT * FROM HATYONETIM.GARAJ d ;

GRANT ALL PRIVILEGES ON HATYONETIM.GOREV TO SDE;
CREATE TABLE SDE.GOREV AS SELECT * FROM HATYONETIM.GOREV d ;

GRANT ALL PRIVILEGES ON HATYONETIM.OLUKMLER TO SDE;
CREATE TABLE SDE.OLUKMLER AS SELECT * FROM HATYONETIM.OLUKMLER d ;

GRANT ALL PRIVILEGES ON HATYONETIM.MINIBUS_HATLARI TO SDE;
CREATE TABLE SDE.MINIBUS_HATLARI AS SELECT * FROM HATYONETIM.MINIBUS_HATLARI d ;

GRANT ALL PRIVILEGES ON HATYONETIM.K_GUZERGAH TO SDE;
CREATE TABLE SDE.K_GUZERGAH AS SELECT * FROM HATYONETIM.K_GUZERGAH d ;

GRANT ALL PRIVILEGES ON HATYONETIM.SEGMENT TO SDE;
CREATE TABLE SDE.SEGMENT AS SELECT * FROM HATYONETIM.SEGMENT d ;

GRANT ALL PRIVILEGES ON HATYONETIM.GUZERGAH_OLUKM_REPORT TO SDE;
CREATE TABLE SDE.GUZERGAH_OLUKM_REPORT AS SELECT * FROM HATYONETIM.GUZERGAH_OLUKM_REPORT d ;


CREATE TABLE "REQUEST_POOL" 
   (	"SERVICE_NAME" VARCHAR2(50), 
	"SERVICE_URL" VARCHAR2(250) NOT NULL ENABLE, 
	"PARAMS" VARCHAR2(50), 
	"FINISHED_DATE" DATE, 
	"CREATED_DATE" DATE DEFAULT sysdate, 
	"STATUS" VARCHAR2(50) DEFAULT 'WAITING');
	
SELECT * FROM sde.REQUEST_POOL rp;


UPDATE SDE.REQUEST_POOL set status = 'FINISHED' WHERE service_name = 'line_{65F3C829-B578-4CAD-A680-87FD97377853}'


INSERT INTO SDE.ST_SPATIAL_REFERENCES (SR_NAME, SRID, 
X_OFFSET, Y_OFFSET, XYUNITS, Z_OFFSET, Z_SCALE, M_OFFSET, 
M_SCALE, MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z, MIN_M, 
MAX_M, CS_ID, CS_NAME, CS_TYPE, ORGANIZATION, 
ORG_COORDSYS_ID, DEFINITION, DESCRIPTION)
VALUES (
 'IETT7932', 
 7932,
 -400,
 -400,
 1000000000, 
 -100000, 
 100000, 
 -100000, 
 100000, 
 9.999E35,
 -9.999E35, 
 9.999E35, 
 -9.999E35, 
 9.999E35, 
 -9.999E35, 
 9.999E35, 
 -9.999E35, 
 7932, 
 'IETT7932',
 'PROJECTED', 
 NULL,
 NULL,
 'GEOGCS["GCS_ITRF_1996",
        DATUM["D_ITRF_1996",
            SPHEROID["GRS_1980",6378137.0,298.257222101]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.017453292519943295]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["central_meridian",30.0],
    PARAMETER["latitude_of_origin",0.0],
    PARAMETER["scale_factor",1],
    PARAMETER["false_easting",500000.0],
    PARAMETER["false_northing",0.0],
    UNIT["m",1.0]]',
 'IETT7932'
);

-- Unlock SDE Account
ALTER USER SDE IDENTIFIED BY "Arc.21042021" ACCOUNT UNLOCK; 

SELECT * FROM sde.ST_SPATIAL_REFERENCES ssr WHERE SRID = 7932;
SELECT * FROM user_sdo_geom_metadata WHERE TABLE_NAME = 'GUZERGAH_GEOLOC';

-- Duraklardaki meseleler:
SELECT * FROM YRDMC_DURAK_DURUMU ydd ; -- aktif pasif
SELECT * FROM YRDMC_DURAK_TIP ydt; -- ACIK DURAK, 
SELECT * FROM YRDMC_FORM_FIZIKI_DURUM yffd; -- FOB BURADA SANIRIM
SELECT * FROM YRDMC_FIZIKI_DURUM yfd;
SELECT * FROM YRDMC_DURAK_KALDIRILDI_MI ydkm;


SELECT * FROM SDE.DURAK