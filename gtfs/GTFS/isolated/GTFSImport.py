# -*- coding: utf-8 -*-
# Esri start of added variables
import os.path
import zipfile

g_ESRI_variable_1 = u'C:\\YAYIN\\PG\\sde_gyy.sde'
# Esri end of added variables

import arcpy

SDE_PATH = g_ESRI_variable_1


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT GTFS Import Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ImportGTFS]


class ImportGTFS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Import GTFS"
        self.description = "Zip file: "
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_gtfs = arcpy.Parameter(
            displayName="Input Zip",
            name="indata",
            datatype="DEFile",
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

        params = [in_gtfs, out_gtfs]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gtfs_zip = parameters[0].valueAsText
        # in_gtfs_zip = os.path.join("data", "gtfs.zip")
        arcpy.AddMessage("Here we go")
        output_folder = arcpy.env.scratchFolder
        output_gdb = arcpy.env.scratchGDB
        arcpy.AddMessage(f"output folder: {output_folder}")
        arcpy.AddMessage(f"output GDB: {output_gdb}")

        # Saving
        zip_extracted_folder = os.path.join(output_folder, 'extracted')
        dataset_name = "IETT_GTFS"
        dataset_path = os.path.join(output_gdb, dataset_name)

        with zipfile.ZipFile(in_gtfs_zip, 'r') as z:
            z.extractall(zip_extracted_folder)
        arcpy.AddMessage("zip file is extracted !")

        if not arcpy.Exists(dataset_path):
            arcpy.CreateFeatureDataset_management(output_gdb, out_name=dataset_name, spatial_reference=4326)
            arcpy.AddMessage("Feature dataset is created !")

        arcpy.transit.GTFSToPublicTransitDataModel(zip_extracted_folder, dataset_path,
                                                   "INTERPOLATE", "NO_APPEND")


# if __name__ == '__main__':
#     igtfs = ImportGTFS()
#     igtfs.execute()
