# Esri start of added imports
import sys, os, arcpy

# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = 'C:\\YAYIN\\GP_REPORT_OUTPUTS'
g_ESRI_variable_2 = 'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables

import os.path

import arcpy
from arcpy import AddMessage as msg

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


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT Report Generator Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ReportGenerator]


class ReportGenerator(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Report Generator"
        self.description = "Sartnamedeki tum raporlarin uretim araci. Bir cogu viewlardan beslenir."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        report_param = arcpy.Parameter(
            displayName="Rapor Tipi",
            datatype="GPString",
            name="Rapor",
            parameterType="Required",
            direction="Input",
        )

        out_excel = arcpy.Parameter(
            displayName="Output Report",
            name="Output",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output"
        )

        report_param.filter.type = "ValueList"
        report_param.filter.list = list(REPORT_ITEMS.keys())

        parameters = [report_param, out_excel]
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
    def fc_to_df(in_fc, input_fields=None, drop_shape=True, query="", skip_nulls=False, null_values=None):
        """Function will convert an arcgis feature class table into a pandas dataframe with an object ID index, and the selected
        input fields. Uses TableToNumPyArray to get initial data.
        :param - in_fc - input feature class or table to convert
        :param - input_fields - fields to input into a da numpy converter function
        :param - drop_shape - drop the shape field from the dataframe
        :param - query - sql like query to filter out records returned
        :param - skip_nulls - skip rows with null values
        :param - null_values - values to replace null values with.
        :returns - pandas dataframe"""
        OIDFieldName = arcpy.Describe(in_fc).OIDFieldName
        msg("OIDFieldName : " + OIDFieldName)

        if input_fields:
            final_fields = [OIDFieldName] + input_fields
        else:
            final_fields = [field.name for field in arcpy.ListFields(in_fc)]
        if drop_shape and u"Shape" in final_fields:
            final_fields.remove(u"Shape")

        # msg("Fields : " + final_fields)
        # np_array = arcpy.da.TableToNumPyArray(in_fc, final_fields, query, skip_nulls, null_values)
        # object_id_index = np_array[OIDFieldName]
        # fc_dataframe = pd.DataFrame(np_array, index=object_id_index, columns=input_fields)
        return final_fields

    def execute(self, parameters, messages):
        """The source code of the tool."""
        report_name = parameters[0].valueAsText
        report_output = os.path.join(arcpy.env.scratchFolder, report_name)  # CAUTION: no extension
        msg("Report output : " + report_output)

        related_view = REPORT_ITEMS[report_name]
        related_view_path = os.path.join(SDE_PATH, DB_SCHEMA + "." + related_view)
        msg("Related view : " + related_view)
        msg("Related view path : " + related_view_path)

        msg("Table to excel is started..")
        report_output += ".xls"
        msg("Report output : " + report_output)
        if os.path.exists(report_output):
            os.remove(report_output)

        arcpy.conversion.TableToExcel(related_view_path, report_output,
                                                       "ALIAS")

        arcpy.SetParameter(1, report_output)
