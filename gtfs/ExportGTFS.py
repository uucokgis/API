# -*- coding: utf-8 -*-
# Esri start of added imports
import os, io

# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables

import os.path

import arcpy
import pandas as pd

SDE_PATH = g_ESRI_variable_1


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT GTFS Export Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ExportGTFS]


class ExportGTFS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export GTFS"
        self.description = "VW_GTFS_DURAK, VW_GTFS_GUZERGAH viewini kullanir"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_layer = arcpy.Parameter(
            displayName="Input Layer",
            name="indata",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        out_gtfs = arcpy.Parameter(
            displayName="GTFS Export",
            name="out_gtfs",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output"
        )

        in_layer.filter.list = ['GUZERGAH', 'DURAK']
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

    def guzergah_gtfs(self, output_folder):
        """
        route_id*, route_short_name*, route_long_name, route_desc, route_type*
        :return:
        """
        out_job_path = os.path.join(output_folder, 'routes.txt')
        guzergah_path = os.path.join(SDE_PATH, 'gyy.sde.VW_GTFS_GUZERGAH')
        guzergah = self.table_to_data_frame(guzergah_path)
        guzergah.drop('row_id', axis=1, inplace=True)

        arcpy.AddMessage("out job path : " + out_job_path)

        with io.open(out_job_path, 'wb') as writer:
            writer.write("route_id, route_short_name, route_long_name, route_desc, route_type \n")

            for index, row in guzergah.iterrows():
                data = str(row.tolist())[1:-1]
                writer.write(data)

        writer.close()

        arcpy.AddMessage("guzergah output path : {0}".format(out_job_path))
        return out_job_path

    def durak_gtfs(self, output_folder):
        """
        stop_id*, stop_code, stop_name*, stop_desc, stop_lat*, stop_lon*,
        location_type
        :return:
        """
        durak_path = os.path.join(SDE_PATH, 'gyy.sde.VW_GTFS_DURAK')
        out_job_path = os.path.join(output_folder, 'stops.txt')
        durak = self.table_to_data_frame(durak_path)
        durak.drop('row_id', axis=1, inplace=True)

        arcpy.AddMessage("out job path : " + out_job_path)

        with io.open(out_job_path, 'wb') as writer:
            writer.write("stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type \n")

            for index, row in durak.iterrows():
                data = str(row.tolist())[1:-1]
                writer.write(data)

        writer.close()
        arcpy.AddMessage("durak output path : {0}".format(out_job_path))
        return out_job_path

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_layer = parameters[0].valueAsText

        output_folder = arcpy.env.scratchWorkspace
        if output_folder.endswith('.gdb'):
            output_folder = arcpy.env.scratchFolder

        if in_layer == 'GUZERGAH':
            out_job_path = self.guzergah_gtfs(output_folder)

        elif in_layer == 'DURAK':
            out_job_path = self.durak_gtfs(output_folder)

        else:
            raise ValueError

        arcpy.SetParameter(1, out_job_path)

        return
