import os.path

import arcpy
from arcpy import AddMessage as msg

NEAR_TABLE_NAME = "GARAJ_DURAK_NEAR"
GARAJ_TABLE_NAME = "SDE.GARAJ"
DURAK_TABLE_NAME = "SDE.DURAK"

FILE_CONNECTION_SDE = r"C:\YAYIN\sde@hatyonetim.sde"
SQL_DISTINCT_ISLETME_BOLGESI = "SELECT DISTINCT(ISLETME_BOLGESI) FROM sde.DURAK"
GEN_NEAR_TABLE = os.path.join(FILE_CONNECTION_SDE, NEAR_TABLE_NAME)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT UPDM Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarajDurakNear]


class GarajDurakNear:
    """

    :dataclass fields
   GARAJ_KODU, DURAK_KODU, XG, YG, XD, YD, MESAFE, SURE

    """


class OluKMTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Garaj Durak Mesafe Aracı"
        self.description = "Garaj -> Durak arasindan routing servisini kullanarak" \
                           "mesafe sure vs. hesaplanir ve " \
                           "GARAJ_DURAK_NEAR tablosu guncellenir"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
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

    @staticmethod
    def delete_gen_near_table():
        if arcpy.Exists(GEN_NEAR_TABLE):
            arcpy.Delete_management(GEN_NEAR_TABLE)
            msg("Generate near table is deleted")

    def garaj_durak_near(self):
        msg("Garaj durak arasi mesafeler Near araci ile kus ucusu hesaplaniyor..")
        garaj_layer = arcpy.MakeFeatureLayer_management(os.path.join(FILE_CONNECTION_SDE, GARAJ_TABLE_NAME),
                                                        out_layer='garaj')
        durak_layer = arcpy.MakeFeatureLayer_management(os.path.join(FILE_CONNECTION_SDE, DURAK_TABLE_NAME),
                                                        out_layer='durak')

        self.delete_gen_near_table()
        gen_near = arcpy.GenerateNearTable_analysis(garaj_layer, durak_layer,
                                                    GEN_NEAR_TABLE,
                                                    '25 Kilometers', 'LOCATION', 'NO_ANGLE', 'ALL', '0', 'PLANAR')
        msg("Near table is created")

        arcpy.JoinField_management(gen_near, 'IN_FID', garaj_layer,
                                   'OBJECTID', fields=[
                'GARAJ_KODU', 'ISLETME_BOLGESI', 'ISLETME_ALT_BOLGESI',  # ORER_GARAJ?
            ])
        arcpy.JoinField_management(gen_near, 'IN_FID', durak_layer,
                                   'OBJECTID', fields=[
                'DURAK_KODU', 'ISLETME_BOLGESI', 'ISLETME_ALT_BOLGESI',  # ORER_GARAJ?
            ])
        msg("Joins are completed")

    def execute(self, parameters, messages):
        """The source code of the tool."""

        return
