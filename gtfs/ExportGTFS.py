# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables

import os.path
import time

import arcpy
import pandas as pd

SDE_PATH = g_ESRI_variable_1


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


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT Durak Degisim Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [DurakDegisimTool]


class DurakDegisimTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Durak Degisim Rapor Araci"
        self.description = "DURAK_DEGISIM_VW viewini kullanir. \n " \
                           "NOT: Eger yeni sutun eklenirse programdaki " \
                           "durak_all_columns degiskenine eklenmesi gerekir."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        ),
        out_gtfs = arcpy.Parameter(
            displayName="GTFS Export",
            name="out_gtfs",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output"
        )

        params = [in_layer, out_gtfs]
        return params

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
        in_layer = parameters[0].valueAsText
        in_layer_name = arcpy.Describe(in_layer).name.encode('utf-8')
        start_time = time.time()

        output_folder = arcpy.env.scratchWorkspace
        if output_folder.endswith('.gdb'):
            output_folder = arcpy.env.scratchFolder

        out_job_path = os.path.join(output_folder, '{0}.txt'.format(in_layer_name))
        arcpy.AddMessage("gtfs output path : {0}".format(out_job_path))

        df = table_to_data_frame(in_layer)
        df = df.head(5)
        arcpy.AddMessage(df.head(5))

        gtfs_objects = []
        # creating GTFS object
        with open(out_job_path, 'w') as writer:
            # iterating rows of the layer
            for index, row in df.iterrows():
                # fields of gtfs
                pass

                #
                result = None
                gtfs_objects.append(result)

        writer.close()
        arcpy.AddMessage("Gecen toplam zaman: {0} saniye".format(time.time() - start_time))

        arcpy.SetParameter(0, out_job_path)

        return
