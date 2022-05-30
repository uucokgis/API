# Esri start of added imports
import asyncio
import os
import sys
# Esri start of added variables

# Esri end of added imports

g_ESRI_variable_1 = 'C:\\YAYIN\\GP_REPORT_OUTPUTS'
g_ESRI_variable_2 = 'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables

import os.path
import aiohttp

import arcpy
import arcgis
from arcgis.features import Feature
from arcpy import AddMessage as msg
import pandas as pd

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
        resp_coords = {'paths': resp_coords}
        line = arcgis.geometry.Polyline(resp_coords)
        line_feature = Feature(line)

        df.loc[oid, 'mesafe'] = mesafe
        df.loc[oid, 'shape'] = line_feature


async def network_requester(df):
    df['mesafe'] = None
    df['shape'] = None

    await asyncio.gather(*[process_url(df, row[1]['objectid'], row[1]['uris']) for
                           row in df[['objectid', 'uris']].iterrows()])
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

    def table_to_data_frame(self, in_table, input_fields=None, where_clause=None):
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

    def execute(self, parameters, messages):
        """The source code of the tool."""
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

        garaj_durak_near_df = self.table_to_data_frame(garaj_durak_near)

        request_uri_list = []

        for _, row in garaj_durak_near_df.iterrows():
            bas_x, bas_y, bit_x, bit_y = float(row['from_x']), float(row['from_y']), \
                                         float(row['near_x']), float(row['near_y']),
            request_uri = network_service_uri.format(bas_x=bas_x, bas_y=bas_y,
                                                     bit_x=bit_x, bit_y=bit_y, ara="")
            request_uri_list.append(request_uri)
        garaj_durak_near_df['uris'] = request_uri_list

        msg(f"Dataframe : {garaj_durak_near_df}")
        msg(f"Columns : {garaj_durak_near_df.columns}")
        columns = ["DURAK_GUID", "GARAJ_GUID", "MESAFE", "SURE"]

        # async processes
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(network_requester(garaj_durak_near_df))
        loop.close()
        msg(f"Dataframe : {garaj_durak_near_df.head(5)}")

# if __name__ == '__main__':
#     dgr = DurakGarajRoute()
#     df = pd.read_excel(r"C:\Users\l4712\PycharmProjects\iettProject\garaj_durak.xlsx")
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(network_requester(df))
#     loop.close()
#
#     print("Dataframe is updated")
