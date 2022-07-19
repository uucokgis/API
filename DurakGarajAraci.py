# Esri start of added imports
import ast
import asyncio
import os
import sys
import time
from itertools import product

import pyproj
# Esri end of added imports
from shapely import wkt

# Esri start of added variables

g_ESRI_variable_1 = 'C:\\YAYIN\\GP_REPORT_OUTPUTS'
g_ESRI_variable_2 = 'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables
from arcgis.features import GeoAccessor
import os.path
import aiohttp
from geopandas import GeoDataFrame
import arcpy
import arcgis
from arcgis.features import Feature
from arcpy import AddMessage as msg
from arcpy import AddWarning as wrn
import pandas as pd
from shapely.geometry import LineString

ITRF96_7932_PROJECTION = """PROJCS["ITRF96 / TM30",GEOGCS["GCS_ITRF_1996",DATUM["D_ITRF_1996",
SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],
PARAMETER["central_meridian",30.0],PARAMETER["scale_factor",1.0],PARAMETER["latitude_of_origin",0.0],
UNIT["m",1.0]]"""

REPORT_ITEMS = {
    "Durak Cephe Olculeri": "VW_DURAKCEPHEOLCULERI_NEW",
    "Duraklar Arasi Mesafe Süre": None,
    "Duraklar için Engelli Erisim Listesi": None,
    "Duraklar": None,
    "Duraklarin Güzergah Raporu": None,
    "Fotograf Olmayan Durak Raporu": None,
    "Garajlar Raporu": None,
    "Güzergah Ölü KM Raporu": None,
    "Güzergahlarin ilk Son Durak Raporu": None,
    "Güzergahsiz Durak Raporu": None,
    "Güzergahtan Bagimsiz Segmentler Raporu": None,
    "Güzergahlar Raporu": None,
    "Hat Basi Hat Sonu Raporu": None,  # sartnamede var appde yok
    "Hatlar Raporu": None,
    "BA Raporu": None,
    # "Proje Alani Raporu",
    # "Ilçe Karti Raporu",
    "Koordinatli Hat Durak Sira Liste Raporu": None,
    "Peronlar Raporu": None,
    # "Güzergah Degisim Raporu",
    # "Durak Degisim Raporu"

}
REPORTS_FOLDER = g_ESRI_variable_1

SDE_PATH = g_ESRI_variable_2
DB_SCHEMA = "gyy.sde"
network_service_uri = "https://cbsproxy.ibb.gov.tr/?networkws&baslangic={bas_x}%7C{bas_y}" \
                      "&ara={ara}" \
                      "&bitis={bit_x}%7C{bit_y}"

garaj_durak_shapes = []


async def process_url(df, oid, url):
    async with aiohttp.ClientSession() as session:
        try:
            resp = await session.get(url)
            data = await resp.json()
            data = str(data['string']['#text'])

            resp_coords, direction = data.split(",@<table cellspacing='0'")
            resp_coords = resp_coords.split(",")
            mesafe_start = direction.find('<b>Mesafe : </b>')
            mesafe_end = direction.find(' m<br></td>')
            mesafe = direction[mesafe_start + 16: mesafe_end].replace(',', '.')
            mesafe = float(mesafe)

            resp_coords = [i.split(' ') for i in resp_coords]
            resp_coords = [(float(i[0]), float(i[1])) for i in resp_coords]
            line_feature = LineString(resp_coords)

            # todo: bura degisecek -> df.at and use index
            df.loc[oid, 'mesafe'] = mesafe
            df.loc[oid, 'shape'] = line_feature

            print(f"Done: {oid}")
        except Exception as err:
            wrn(f"cbsproxy error : {str(err)}")


async def network_requester(df, oid='objectid'):
    df['mesafe'] = None
    df['shape'] = None

    await asyncio.gather(*[process_url(df, row[1][oid], row[1]['uris']) for
                           row in df[[oid, 'uris']].iterrows()])
    return df


def table_to_data_frame(in_table, input_fields=None, where_clause=None):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""
    try:
        OIDFieldName = arcpy.Describe(in_table).OIDFieldName
        if input_fields:
            final_fields = [OIDFieldName] + input_fields
        else:
            final_fields = [field.aliasName for field in arcpy.ListFields(in_table)]

        try:
            data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]

        except RuntimeError:
            final_fields = [f.name for f in arcpy.ListFields(in_table)]
            data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]

        fc_dataframe = pd.DataFrame(data, columns=final_fields)
        fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=False)

        return fc_dataframe
    except OSError as err:
        arcpy.AddError("Veritabaninda {0} view'i bulunamadigi icin rapor uretilemedi. \n".format(in_table))
        arcpy.AddError("Hata : {0}".format(err))


def prepare_network_requests(df):
    request_uri_list = []

    for _, row in df.iterrows():
        bas_x, bas_y, bit_x, bit_y = row['from_x'], row['from_y'], row['near_x'], row['near_y']
        request_uri = network_service_uri.format(bas_x=bas_x, bas_y=bas_y,
                                                 bit_x=bit_x, bit_y=bit_y, ara="")
        request_uri_list.append(request_uri)
    df['uris'] = request_uri_list

    return df


class Toolbox(object):
    """
    10.	Ek olarak 4 adet tablo düşünülmektedir;
a.	-- DURAKTAN DURAGA: DURAK_DURAK_ROTA:  Tool2: HatbasiHatsonuDurakRota
        BIR HAT SONU DURAGININ DIGER TUM HAT BASI DURAKLARINA
        + BIR HAT BASI DURAGININ DIGER TUM HAT SONU DURAKLARINA

b.	-- DURAKTAN GARAJA: DURAK_GARAJ_ROTA:   Tool1: DurakGarajRoute
c.	-- GARAJDAN GARAJA: GARAJ_GARAJ_ROTA -- BAKIM ICIN VS.
d.	-- GARDAN DURAKLARA GAR_DURAK_ROTA (AMA SADECE HAT BASI VEYA HAT SONU OLAN DURAKLAR)

    """

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT Data Generator Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [DurakGarajRoute]


class DurakGarajRoute(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Durak Garaj Route Generator"
        self.description = "Durak garaj rotalarini hesaplayip DURAK_GARAJ_ROTA tablosunu gunceller."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        buffer_distance = arcpy.Parameter(
            displayName="Tampon Mesafesi",
            datatype="GPLong",
            name="Buffer",
            parameterType="Required",
            direction="Input",
        )

        parameters = [buffer_distance]
        return parameters

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)

        buffer_distance = parameters[0]
        # buffer_distance = parameters[0].valueAsText
        msg(f"Buffer tampon mesafesi : {buffer_distance}")

        durak_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK")
        garaj_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ")
        garaj_durak_route = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_DURAK_ROUTE")
        # garaj_durak_near = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_DURAK_NEAR")
        durak_garaj_vw = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_GARAJ_VIEW")

        msg("Durak tablosu : " + durak_table)
        msg("Garaj tablosu : " + garaj_table)

        durak_garaj_df = table_to_data_frame(durak_garaj_vw)
        # column formatting
        durak_garaj_df['durak_y'] = durak_garaj_df['durak_y'].apply(lambda x: x.split(')')[0]).astype(float)
        durak_garaj_df['garaj_y'] = durak_garaj_df['garaj_y'].apply(lambda x: x.split(')')[0]).astype(float)

        durak_garaj_df['durak_x'] = durak_garaj_df['durak_y'].astype(float)
        durak_garaj_df['garaj_x'] = durak_garaj_df['garaj_x'].apply(lambda x: x.split(')')[0]).astype(float)

        durak_garaj_df = durak_garaj_df.head(50)
        durak_garaj_df.rename(
            columns={"durak_x": "from_x", "durak_y": "from_y", "garaj_x": "near_x", "garaj_y": "near_y"},
            inplace=True)
        garaj_durak_df = prepare_network_requests(durak_garaj_df)

        msg(f"Dataframe : {garaj_durak_df}")
        msg(f"Columns : {garaj_durak_df.columns}")
        columns = ["DURAK_GUID", "GARAJ_GUID", "MESAFE", "SURE"]

        # async processes
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(network_requester(garaj_durak_df, oid='row_id'))
        loop.close()
        msg("Async process is finished.")
        msg(f"Dataframe: {garaj_durak_df['shape'].head(5)}")

        garaj_durak_df['shape'] = garaj_durak_df['shape'].apply(lambda x: x.wkt)
        msg(f"Dataframe: {garaj_durak_df['shape'].head(5)}")

        gdf = GeoDataFrame(garaj_durak_df, crs=crs_7932,
                           geometry=garaj_durak_df['shape'].apply(wkt.loads))
        sdf = GeoAccessor.from_geodataframe(gdf)
        sdf.spatial.to_featureclass(garaj_durak_route, overwrite=True)


class HatbasiHatsonuDurakRota(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Hat basi hat sonu Route Generator"
        self.description = "Bir hat sonu duraginin diger tum hat basi duraklarina + \n " \
                           "Bir hat basi duraginin diger tum hat sonu duraklarina"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        buffer_distance = arcpy.Parameter(
            displayName="Tampon Mesafesi",
            datatype="GPLong",
            name="Buffer",
            parameterType="Optional",
            direction="Input",
        )

        parameters = [buffer_distance]
        return parameters

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        start_time = time.time()
        crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
        # buffer_distance = parameters[0].valueAsText
        buffer_distance = parameters[0]
        msg(f"Buffer tampon mesafesi :{buffer_distance} ")

        hat_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.HATBASBITDURAK_VIEW_COMBINATION")
        hat_durak_route_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.HATBASBITDURAK_ROUTE")
        hat_df = table_to_data_frame(hat_table)

        # data filtering
        hat_df['hatbasdurak'] = hat_df['hatbasdurak'].astype(int)
        hat_df['hatbitdurak'] = hat_df['hatbitdurak'].astype(int)
        hat_df_bas_son = hat_df.rename(columns={
            "bas_durak_x": "from_x",
            "bas_durak_y": "from_y",
            "bit_durak_x": "near_x",
            "bit_durak_y": "near_y"
        })
        hat_df_bas_son = prepare_network_requests(hat_df_bas_son)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(network_requester(hat_df_bas_son, oid='row_id'))
        loop.close()

        gdf = GeoDataFrame(hat_df_bas_son, crs=crs_7932,
                           geometry=hat_df_bas_son['shape'].apply(wkt.loads))
        sdf = GeoAccessor.from_geodataframe(gdf)
        sdf.spatial.to_featureclass(hat_durak_route_table, overwrite=True)


class GarajGarajRoute(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Hat basi hat sonu Route Generator"
        self.description = "Bir hat sonu duraginin diger tum hat basi duraklarina + \n " \
                           "Bir hat basi duraginin diger tum hat sonu duraklarina"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        buffer_distance = arcpy.Parameter(
            displayName="Tampon Mesafesi",
            datatype="GPLong",
            name="Buffer",
            parameterType="Optional",
            direction="Input",
        )

        parameters = [buffer_distance]
        return parameters

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        start_time = time.time()
        crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
        DURAK_GARAJ_VW = f"{DB_SCHEMA}.DURAK_GARAJ_VW"
        # buffer_distance = parameters[0].valueAsText

        durak_garaj_df = table_to_data_frame(DURAK_GARAJ_VW)
        isletme_combinations = []
        for index, isletme_df in durak_garaj_df.groupby('d_isletme_bolgesi'):
            isletme_df = prepare_network_requests(isletme_df)
            # async processes
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(network_requester(isletme_df))
            loop.close()
            msg("Async process is finished.")
            msg(f"Dataframe: {isletme_df['shape'].head(5)}")

            isletme_df['shape'] = isletme_df['shape'].apply(lambda x: x.wkt)
            msg(f"Dataframe: {isletme_df['shape'].head(5)}")

            gdf = GeoDataFrame(isletme_df, crs=crs_7932,
                               geometry=isletme_df['shape'].apply(wkt.loads))
            sdf = GeoAccessor.from_geodataframe(gdf)
            # todo:
            # sdf.spatial.to_featureclass(r"C:\YAYIN\PG\BaseTables.gdb\garajduraktest")
            msg(f"Dataframe : {sdf.head(5)}")

            isletme_combinations.append(sdf)


class GarDurakRoute(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Gar Durak Route Generator"
        self.description = "GARDAN DURAKLARA GAR_DURAK_ROTA (AMA SADECE HAT BASI VEYA HAT SONU OLAN DURAKLAR)"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        buffer_distance = arcpy.Parameter(
            displayName="Tampon Mesafesi",
            datatype="GPLong",
            name="Buffer",
            parameterType="Optional",
            direction="Input",
        )

        parameters = [buffer_distance]
        return parameters

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        start_time = time.time()
        crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
        HATBASBIT_DURAK_GAR_VW = f"{DB_SCHEMA}.HATBASBITDURAK_GAR_VW"


if __name__ == '__main__':
    # hhdr = DurakGarajRoute()
    # hhdr.execute([None], None)

    hhdr = HatbasiHatsonuDurakRota()
    hhdr.execute([None], None)