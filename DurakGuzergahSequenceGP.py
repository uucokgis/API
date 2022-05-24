import os.path

import arcpy

sde_path = r"C:\YAYIN\PG\sde_gyy.sde"
dbschema = "gyy.sde"

durak_path = os.path.join(sde_path, "{0}.{1}".format(dbschema, "DURAK"))
guzergah_path = os.path.join(sde_path, "{0}.{1}".format(dbschema, "GUZERGAH_GEOLOC_MAP"))
spatial_out = os.path.join(sde_path, "DURAK_GUZERGAH_SJ")

if arcpy.Exists(spatial_out):
    arcpy.Delete_management(spatial_out)

arcpy.SpatialJoin_analysis("gyy.sde.DURAK",
                           "gyy.sde.GUZERGAH_GEOLOC_MAP",
                           r"C:\Users\karpuz\Documents\ArcGIS\Projects\PG\PG.gdb\gyy_SpatialJoin",
                           "JOIN_ONE_TO_MANY", "KEEP_ALL",
                           match_option='INTERSECT',
                           field_mapping='durak_kodu "durak_kodu" true true false 4 Long 0 10,First'
                                         ',#,gyy.sde.DURAK,durak_kodu,-1,-1;id "id" true true false '
                                         '8 Double 8 38,First,#,gyy.sde.GUZERGAH_GEOLOC_MAP,id,-1,-1;'
                                         'guzergah_id "guzergah_id" true true false 8 Double 8 38,First,'
                                         '#,gyy.sde.GUZERGAH_GEOLOC_MAP,guzergah_id,-1,-1'
                           )
