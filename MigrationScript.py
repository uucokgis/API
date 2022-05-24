# @Author: Umut Ucok
# Golden Rule: Projeyle alakali bildigin seyler kadar calistir.
import os
from os.path import split

import arcpy
import pandas as pd

base_tables = [
    "PERON",
    "PERON_ALANI",
    "DURAK",
    "GUZERGAH",
    "GUZERGAH_GEOLOC_MAP",
    "HAT",
    "GARAJ",
    "GARAJ_ALANI",
    "GAR",
    "GAR_ALANI",
    "DURAK_BILGI",
    "MAHALLELER",
    "ILCELER",
    "BOLGE",
    "DEPO",
    "DURAK_AKTARMA_NOKTALARI",
    "DURAK_DETAY"]
cog_tables = [
    "PLN_RAYLI_SISTEM_HAT",
    "MINIBUS_HATLARI",
    "PLN_RAYLI_SISTEM_ISTASYON",
    "MEVCUT_RAYLI_ISTASYONLARI",
    "GUZERGAH_GEOLOC",
    "MEVCUT_METROBUS_ISTASYON",
    "DENIZ_ISKELE_NOKTALARI",
    "MEVCUT_RAYLI_SISTEM_HATLARI",
    "MEVCUT_METROBUS_HATTI"
]

gdb_path = r'C:\YAYIN\PG\BaseTables.gdb'
sde_path = r"C:\YAYIN\PG\sde_gyy.sde"
itrf_96 = 'PROJCS["ITRF96 / TM30",GEOGCS["GCS_ITRF_1996",DATUM["D_ITRF_1996",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],PARAMETER["central_meridian",30.0],PARAMETER["scale_factor",1.0],PARAMETER["latitude_of_origin",0.0],UNIT["m",1.0]]'
rship_xls_file = r""  # todo:
sql_view_folder = r"C:\Users\l4712\PycharmProjects\iettProject\Scripts\prodviews"  # todo:
dbschema = "gyy.sde"


## Put into map
def put_into_map():
    bulunamayanlar = []
    others = []

    for table in base_tables:
        arcpy.AddMessage("table : " + table)
        print("table : " + table)
        src_table = os.path.join(r'Database Connections\TESTHATYONETIM.sde', 'HATYONETIM.{0}'.format(table))
        layer_name = table

        try:
            arcpy.MakeFeatureLayer_management(src_table, layer_name)

        except Exception as err:
            if str(err).count('does not exist'):
                print("Bulunamadi : " + str(err))
                bulunamayanlar.append(table)
            else:
                others.append(table)
            # print("Error : " + str(err))


## Export
def export():
    layers = []
    mxd = arcpy.mapping.MapDocument("CURRENT")
    for lyr in arcpy.mapping.ListLayers(mxd):
        layers.append(lyr.name)

    for lyr in layers:
        cnt = arcpy.GetCount_management(lyr).getOutput(0)
        cnt = int(cnt)
        if cnt == 0:
            print(lyr + "is 0")

        else:
            try:
                arcpy.FeatureClassToFeatureClass_conversion(lyr,
                                                            gdb_path, lyr)
            except Exception as err:
                err = str(err)
                print(lyr + "hata : " + err)


## Define projection
def define_and_project():
    def define():
        layers = []
        p = arcpy.mp.ArcGISProject("CURRENT")
        m = p.listMaps()[0]
        for lyr in m.listLayers():
            layers.append(lyr)

        for lyr in layers:
            print("layer : " + lyr.name)
            try:
                arcpy.DefineProjection_management(
                    lyr.name, itrf_96
                )
            except Exception as err:
                err = str(err)
                print(lyr.name + "hata : " + err)

    def project():
        for table in cog_tables:
            table = os.path.join(sde_path, "{0}".format(table))
            out_table = os.path.join(sde_path, "{0}_projected".format(table))
            print("Table : " + table)
            print("Out Table : " + out_table)
            try:
                arcpy.DefineProjection_management(
                    table, 4326
                )
                if arcpy.Exists(out_table):
                    arcpy.Delete_management(out_table)
                arcpy.Project_management(table, out_table,
                                         "PROJCS['ITRF96 / TM30',GEOGCS['GCS_ITRF_1996',DATUM['D_ITRF_1996',"
                                         "SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],"
                                         "PROJECTION['Transverse_Mercator'],PARAMETER['false_easting',500000.0],PARAMETER['false_northing',0.0],"
                                         "PARAMETER['central_meridian',30.0],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',0.0],UNIT['m',1.0]]",
                                         "'ITRF_2000_To_WGS_1984 + ITRF_1996_To_ITRF_2000_1'",
                                         "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],"
                                         "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
                arcpy.Delete_management(table)
                arcpy.Rename_management(out_table, table)

            except Exception as err:
                print("{0} table - HATA : " + str(err))

    define()
    project()


## Relationship
"""
PERON -> PERON_ALANI -> 1-1
GARAJ -> GARAJ_ALANI -> 1-1
GAR -> GAR_ALANI -> 1-1
DURAK_SORUN -> DURAK -> M-1
DURAK_BILGI -> DURAK -> M-1
DURAK -> IL & ILCE & MAHALLE M-1
DURAK_AKTARMA_NOKTALARI -> DURAK 1-M
BOLGE -> ILCE -> 1-M
BA_RAPORU -> DURAK (DURAK_KODU_A & B) -> 1-1
BA_RAPORU -> HAT (HAT_KODU) -> M-1 ? HAT_KODU, GUZERGAH_ID, BITIS_GUZERGAH_ID, BITIS_DURAK_KODU, ... BOS

KONUSALIM:
HAT -> GARAJ M-1 MIDIR?
GUZERGAH -> GARAJ ?
GOREV -> HAT (BU ILGINC)
DURAK -> DURAK_GARAJ_ROTA (* BIZ ACACAGIZ, SUTUNLARINI KONUSALIM)
MEVCUT_METROBUS_IISTASYON -> ILCE ** BU NORMALDE TEXT VE DIGERLERINDE (MINIBUS DENIZ ISKELE VS.) YOK AMA HEPSINE KOYALIM
DURAK -> PERON (GUNCELDE PERON_KODU VAR AMA ILISKI CIZILMEMIS)
DURAK_GOZLEM?
BA_RAPORU'NUN SUTUNLARINDAKI HAT | DURAK ILISKILERI
HAT'TAKI HAT_BASI / HAT_SONU ASLINDA ORADAKI DURAGIN KOORDINATLARI MI? HER HAT BASI DURAGA MI BAGLANIR?


* DURAKLA ILGILI DIGER ARA TABLOLARI DOMAIN YAPACAGIZ.

"""


def create_relationships():
    df = pd.read_excel(rship_xls_file)
    for index, row in df.iterrows():
        kaynak, hedef, rstype = row['kaynak'], row['hedef'], row['rstype']
        kaynak_p = os.path.join(sde_path, f"{0}.{1}".format(dbschema, kaynak))
        hedef_p = os.path.join(sde_path, f"{0}.{1}".format(dbschema, kaynak))
        rsout = os.path.join(sde_path, f"{0}_{1}_RS".format(kaynak, hedef))

        try:
            arcpy.CreateRelationshipClass_management(
                kaynak_p, hedef_p, rsout, "SIMPLE", "TO_{0}".format(hedef), "TO_{0}".format(kaynak),
                "BOTH", cardinality=rstype
            )

        except Exception as err:
            print("{0} - {1} HATA : ".format(kaynak, hedef) + str(err))


## Create Views
def create_views(only_list=False):
    views = []
    sql_files = [os.path.join(sql_view_folder, i) for i in os.listdir(sql_view_folder)]
    for sql_f in sql_files:
        p, fname = split(sql_f)
        if fname != 'Report_1.sql':
            continue

        vwname = fname.split(".")[0]

        try:
            with open(sql_f, 'r') as reader:
                sql_sentence = reader.readlines()
                sql_sentence = " ".join([i for i in sql_sentence]).replace('\n', ' ').replace('  ', ' ')
                select_sql_start = sql_sentence.index('AS SELECT')
                select_sql = sql_sentence[select_sql_start: select_sql_start + 3]
                print("Select SQL : " + select_sql)
                arcpy.AddMessage("Select SQL : " + select_sql)

                if not only_list:
                    arcpy.CreateDatabaseView_management(
                        sde_path, vwname, select_sql
                    )
                views.append(os.path.join(sde_path, "{0}.{1}".format(dbschema, vwname)))
        except Exception as err:
            print("{0} -- ".format(sql_f) + str(err))


## Creating map with views
def create_map_view_views():
    pass


if __name__ == '__main__':
    create_views()
