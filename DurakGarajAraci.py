# Esri start of added imports
import ast
import asyncio
import os
import sys
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
        resp = await session.get(url)
        data = await resp.json()
        data = str(data['string']['#text'])
        print("Done")

        resp_coords, direction = data.split(",@<table cellspacing='0'")
        resp_coords = resp_coords.split(",")
        mesafe_start = direction.find('<b>Mesafe : </b>')
        mesafe_end = direction.find(' m<br></td>')
        mesafe = direction[mesafe_start + 16: mesafe_end].replace(',', '.')
        mesafe = float(mesafe)

        resp_coords = [i.split(' ') for i in resp_coords]
        resp_coords = [(float(i[0]), float(i[1])) for i in resp_coords]
        line_feature = LineString(resp_coords)

        df.loc[oid, 'mesafe'] = mesafe
        df.loc[oid, 'shape'] = line_feature


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

        sys.exit(0)


def prepare_network_requests(df):
    # todo: uncompatible with durak garaj route test
    request_uri_list = []

    for _, row in df.iterrows():
        bas_x, bas_y, bit_x, bit_y = row['from_x'], row['from_y'], row['near_x'], row['near_y']
        request_uri = network_service_uri.format(bas_x=bas_x, bas_y=bas_y,
                                                 bit_x=bit_x, bit_y=bit_y, ara="")
        request_uri_list.append(request_uri)
    df['uris'] = request_uri_list

    return df


class Toolbox(object):
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
            displayName="Tampon Mesafes'",
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

        buffer_distance = parameters[0].valueAsText
        msg("Buffer tampon mesafesi : " + buffer_distance)

        durak_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK")
        garaj_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ")
        garaj_durak_route = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_DURAK_ROUTE")
        garaj_durak_near = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_DURAK_NEAR")

        msg("Durak tablosu : " + durak_table)
        msg("Garaj tablosu : " + garaj_table)

        durak_layer = arcpy.MakeFeatureLayer_management(durak_table, "DURAK_LAYER")
        garaj_layer = arcpy.MakeFeatureLayer_management(garaj_table, "GARAJ_LAYER")
        garaj_durak_layer = arcpy.MakeFeatureLayer_management(garaj_durak_route, "GARAJ_DURAK_LAYER")
        msg("Making layer is finished.")

        arcpy.GenerateNearTable_analysis(
            garaj_layer,
            durak_layer,
            garaj_durak_near,
            f"{buffer_distance} Meters",
            "LOCATION", "NO_ANGLE", "ALL", 0, "PLANAR"
        )
        arcpy.DeleteField_management(
            garaj_durak_near, drop_field=['NEAR_DIST', 'NEAR_RANK']
        )
        msg("Generate near + drop fields are finished. ")

        garaj_durak_near_df = table_to_data_frame(garaj_durak_near)
        garaj_durak_near_df = prepare_network_requests(garaj_durak_near_df)

        msg(f"Dataframe : {garaj_durak_near_df}")
        msg(f"Columns : {garaj_durak_near_df.columns}")
        columns = ["DURAK_GUID", "GARAJ_GUID", "MESAFE", "SURE"]

        # async processes
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(network_requester(garaj_durak_near_df))
        loop.close()
        msg("Async process is finished.")
        msg(f"Dataframe: {garaj_durak_near_df['shape'].head(5)}")

        garaj_durak_near_df['shape'] = garaj_durak_near_df['shape'].apply(lambda x: x.wkt)
        msg(f"Dataframe: {garaj_durak_near_df['shape'].head(5)}")

        gdf = GeoDataFrame(garaj_durak_near_df, crs=crs_7932,
                           geometry=garaj_durak_near_df['shape'].apply(wkt.loads))
        sdf = GeoAccessor.from_geodataframe(gdf)
        # todo:
        sdf.spatial.to_featureclass(r"C:\YAYIN\PG\BaseTables.gdb\garajduraktest")
        msg(f"Dataframe : {sdf.head(5)}")


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
            displayName="Tampon Mesafes'",
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

    @staticmethod
    def get_combination(isletme_df):
        hatbasidurak_bs_df = pd.DataFrame(list(product(isletme_df['hatbasdurak'], isletme_df['hatbitdurak'])))
        hatbasidurak_bs_df.drop_duplicates(inplace=True)
        hatbasidurak_bs_df.rename(columns={0: 'hatbasdurak', 1: 'hatbitdurak'}, inplace=True)
        hatbasidurak_bs_df = pd.merge(hatbasidurak_bs_df, isletme_df, left_on='hatbitdurak', right_on='hatbitdurak')
        hatbasidurak_bs_df = hatbasidurak_bs_df[["hatbasdurak", "hatbitdurak_x", "bas_durak_x", "bas_durak_y"]]
        hatbasidurak_bs_df.rename(columns={"hatbitdurak_x": 'hatbitdurak'}, inplace=True)
        hatbasidurak_bs_df.drop_duplicates(inplace=True)

        hatbasidurak_bs_df = pd.merge(hatbasidurak_bs_df, isletme_df, left_on='hatbitdurak', right_on='hatbitdurak')
        hatbasidurak_bs_df = hatbasidurak_bs_df[['hatbasdurak_x', 'hatbitdurak', 'bitdurak_x', 'bit']]
        hatbasidurak_bs_df = hatbasidurak_bs_df[hatbasidurak_bs_df[["hatbasdurak", "hatbitdurak_x", "bas_durak_x", "bas_durak_y"]]]

        return hatbasidurak_bs_df

    def execute(self, parameters, messages):
        """The source code of the tool."""
        crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
        # buffer_distance = parameters[0].valueAsText
        buffer_distance = parameters[0]
        msg(f"Buffer tampon mesafesi :{buffer_distance} ")

        durak_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_COORD_VW")
        hat_table = os.path.join(SDE_PATH, f"{DB_SCHEMA}.hatbasbitdurak_vw")
        hat_df = table_to_data_frame(hat_table)
        durak_df = table_to_data_frame(durak_table)

        # data filtering
        hat_df = hat_df[hat_df['hatbasdurak'] != 0]
        hat_df['hatbasdurak'] = hat_df['hatbasdurak'].astype(int)
        hat_df['hatbitdurak'] = hat_df['hatbitdurak'].astype(int)

        combinations = []
        for index, isletme in hat_df.groupby('ana_isletme_bolgesi'):
            hatbasidurak_bs_df = self.get_combination(isletme)
            hatbasidurak_bs_df.drop(columns=[i for i in hatbasidurak_bs_df.columns if i not in (
                'first_col_x', 'last_col_x', 'bas_durak_x_x', 'bas_durak_y_x', 'bit_durak_x', 'bit_durak_y')],
                                    inplace=True)
            hatbasidurak_bs_df.rename(columns={
                'bas_durak_x_x': 'from_x',
                'bas_durak_y_x': 'from_y',
                'bit_durak_x': 'near_x',
                'bit_durak_y': 'near_y'}, inplace=True)

            hatbasidurak_sb_df = self.get_combination(isletme, 'hatbitdurak', 'hatbasdurak')
            hatbasidurak_sb_df.rename(columns={
                'bas_durak_x': 'from_x',
                'bas_durak_y': 'from_y',
                'bit_durak_x': 'near_x',
                'bit_durak_y': 'near_y'}, inplace=True)

            msg(f"Kombinasyon sayisi  BAS -> SON: {len(hatbasidurak_bs_df)}")
            msg(f"Kombinasyon sayisi  SON -> BAS: {len(hatbasidurak_sb_df)}")

            # type conversion and y cleaning due to sql substring
            hatbasidurak_bs_df['from_y'] = hatbasidurak_bs_df['from_y'].apply(lambda x: float(x[:-1]))
            hatbasidurak_bs_df['near_y'] = hatbasidurak_bs_df['near_y'].apply(lambda x: float(x[:-1]))
            hatbasidurak_bs_df['near_x'] = hatbasidurak_bs_df['near_x'].astype(float)
            hatbasidurak_bs_df['from_x'] = hatbasidurak_bs_df['from_x'].astype(float)

            hatbasidurak_sb_df['from_y'] = hatbasidurak_bs_df['from_y'].apply(lambda x: float(x[:-1]))
            hatbasidurak_sb_df['near_y'] = hatbasidurak_sb_df['near_y'].apply(lambda x: float(x[:-1]))
            hatbasidurak_bs_df['near_x'] = hatbasidurak_sb_df['near_x'].astype(float)
            hatbasidurak_sb_df['from_x'] = hatbasidurak_sb_df['from_x'].astype(float)

            hatbasidurak_bs_df = prepare_network_requests(hatbasidurak_bs_df)
            hatbasidurak_sb_df = prepare_network_requests(hatbasidurak_sb_df)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(network_requester(hatbasidurak_df, oid='rowid'))
        loop.close()
        msg("Async process is finished !")
        # hatbasidurak_df['shape'] = hatbasidurak_df['shape'].apply(lambda x: x.wkt)
        # msg(f"Dataframe: {hatbasidurak_df['shape'].head(5)}")
        #
        # gdf = GeoDataFrame(hatbasidurak_df, crs=crs_7932,
        #                    geometry=hatbasidurak_df['shape'].apply(wkt.loads))
        # sdf = GeoAccessor.from_geodataframe(gdf)

        # todo:
        sdf.spatial.to_featureclass(r"C:\YAYIN\PG\BaseTables.gdb\hatbasbitduraktest")
        msg(f"Dataframe: {sdf.head(5)}")


if __name__ == '__main__':
    # df = pd.read_excel(r"C:\Users\l4712\PycharmProjects\iettProject\hatbasihatsonudurak.xlsx")
    # print(df)
    hhdr = HatbasiHatsonuDurakRota()
    hhdr.execute([None], None)
