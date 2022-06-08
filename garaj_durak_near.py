import os.path

import arcpy
from arcpy import AddMessage as msg
from arcgis import GIS
import arcgis

NEAR_TABLE_NAME = "GARAJ_DURAK_NEAR"
GARAJ_TABLE_NAME = "SDE.GARAJ"
# GARAJ_SERVICE_URI = ""
DURAK_TABLE_NAME = "SDE.DURAK"
# DURAK_SERVICE_NAME = ""
PORTAL_USERNAME = 'iettupdm'
PORTAL_PWD = 'm7r[?wF~zuPdTrL<'
FUTURE_DECISION = False  # False: Synchronized. Service will be awaited to get the result.
FILE_CONNECTION_SDE = r"C:\YAYIN\sde@hatyonetim.sde"
SQL_DISTINCT_ISLETME_BOLGESI = "SELECT DISTINCT(ISLETME_BOLGESI) FROM sde.DURAK"
GEN_NEAR_TABLE = os.path.join(FILE_CONNECTION_SDE, NEAR_TABLE_NAME)
agis = GIS(username=PORTAL_USERNAME,
           password=PORTAL_PWD)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT UPDM Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarajDurakNear]


class GarajDurakNear(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        # GARAJ_KODU, DURAK_KODU, XG, YG, XD, YD, MESAFE, SURE
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

    @staticmethod
    def get_garaj_layers():
        garaj_layer = arcpy.MakeFeatureLayer_management(os.path.join(FILE_CONNECTION_SDE, GARAJ_TABLE_NAME),
                                                        out_layer='garaj')
        durak_layer = arcpy.MakeFeatureLayer_management(os.path.join(FILE_CONNECTION_SDE, DURAK_TABLE_NAME),
                                                        out_layer='durak')

        return garaj_layer, durak_layer

    @staticmethod
    def get_garaj_featureset():
        garaj_fset = arcgis.features.FeatureSet(

        )

        durak_fset = arcgis

        return garaj_fset, durak_fset

    def garaj_durak_near(self):
        msg("Garaj durak arasi mesafeler Near araci ile kus ucusu hesaplaniyor..")
        garaj_layer, durak_layer = self.get_garaj_layers()

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

    def garaj_durak_route(self):
        msg("Durak arasi mesafeler routing ile hesaplaniyor")
        garaj_layer, durak_layer = self.get_garaj_layers()
        route_fset = arcgis.choose_best_facilities("MaximizeCoverage", durak_layer,
                                                   max_travel_range=10000,
                                                   travel_mode='Driving Distance',
                                                   travel_direction='FacilityToDemand',
                                                   required_facilities_layer=garaj_layer,
                                                   gis=agis,
                                                   future=FUTURE_DECISION
                                                   )

    def execute(self, parameters, messages):
        """The source code of the tool."""
        self.garaj_durak_near()
        self.garaj_durak_route()
        return


if __name__ == '__main__':
    GarajDurakNear.execute(None, None, None)


td.KONMA_TARIHI != tde.KONMA_TARIHI OR
td.SOKULME_TARIHI != tde.SOKULME_TARIHI OR
td.AKTIF_DURUMU != tde.AKTIF_DURUMU OR
td.MODUL_ADEDI != tde.MODUL_ADEDI OR
td.KALDIRIM_GENISLIGI != tde.KALDIRIM_GENISLIGI OR
td.ADRES != tde.ADRES OR
td.ACIKLAMA != tde.ACIKLAMA OR
td.DURAKLAMA_DURUMU != tde.DURAKLAMA_DURUMU OR
td.ILID != tde.ILID OR
td.ILCEID != tde.ILCEID OR
td.MAHALLEID != tde.MAHALLEID OR
td.DURAK_KISA_ADI != tde.DURAK_KISA_ADI OR
td.LEVHA_VAR != tde.LEVHA_VAR OR
td.PERON_KODU != tde.PERON_KODU OR
td.MODUL_DURAK_DURUMU != tde.MODUL_DURAK_DURUMU OR
td.DURAK_KUME_ID != tde.DURAK_KUME_ID OR
td.PERON_DURAGI != tde.PERON_DURAGI OR
td.DURUMU != tde.DURUMU OR
td.FIZIKI_DURUM != tde.FIZIKI_DURUM OR
td.KALDIRILDI_MI != tde.KALDIRILDI_MI OR
td.YRDMC_FORM_FIZIKI_DURUM != tde.YRDMC_FORM_FIZIKI_DURUM OR
td.ENGELLI_RAMPA != tde.ENGELLI_RAMPA OR
td.ENGELLI_KULLANIM != tde.ENGELLI_KULLANIM OR
td.AKILLI_DURAK_DURUMU != tde.AKILLI_DURAK_DURUMU OR
td.ABONELIK_DURUMU != tde.ABONELIK_DURUMU OR
td.ENERJI_DURUMU != tde.ENERJI_DURUMU OR
td.ELEKTRIK_DURUMU != tde.ELEKTRIK_DURUMU OR
td.CEP_VAR != tde.CEP_VAR OR
td.SOFOR_DEGISIM_NOKTASI != tde.SOFOR_DEGISIM_NOKTASI OR
td.IKMAL_NOKTASI_TIPI != tde.IKMAL_NOKTASI_TIPI OR
td.ISLETME_BOLGESI != tde.ISLETME_BOLGESI OR
td.ISLETME_ALT_BOLGESI != tde.ISLETME_ALT_BOLGESI OR
td.MODUL_DURAK_ID != tde.MODUL_DURAK_ID