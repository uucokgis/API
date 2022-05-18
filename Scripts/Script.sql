-- create lib for sde
CREATE OR REPLACE LIBRARY st_shapelib AS 'C:\app\karpuz\product\11.2.0\client_32\BIN\st_shapelib.dll';

-- permissions for sde
GRANT EXECUTE ON dbms_pipe TO public;
GRANT EXECUTE ON dbms_lock TO public;
GRANT EXECUTE ON dbms_lob TO public;
GRANT EXECUTE ON dbms_utility TO public;
GRANT EXECUTE ON dbms_sql TO public;
GRANT EXECUTE ON utl_raw TO public;

DROP VIEW VW_KOORD_HAT_D_SIRA_LISTE;












