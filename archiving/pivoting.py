import os.path

import arcpy
import pandas as pd

SDE_PATH = r"C:\YAYIN\PG\sde_gyy.sde"


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
        self.label = "Durak Degisim Rapor Aracı"
        self.description = "DURAK_DEGISIM_VW viewini kullanir. \n " \
                           "NOT: Eger yeni sutun eklenirse programdaki " \
                           "durak_all_columns degiskenine eklenmesi gerekir."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        out_excel = arcpy.Parameter(
            displayName="Durak Degisim Raporu",
            name="out_excel",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output"
        )

        return [out_excel]

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        durak_degisim_path = os.path.join(SDE_PATH, 'sde.DURAK_DEGISIM_VW')

        df = table_to_data_frame(durak_degisim_path)
        arcpy.AddMessage(df.head(5))

        data = []
        durak_all_columns = ['adi', 'aciklama', 'durak_kodu', 'yon_bilgisi', 'modul_adedi', 'kaldirim_genisligi',
                             'adres', 'ilid', 'ilceid', 'mahalleid', 'durak_kisa_adi', 'levha_var', 'peron_kodu',
                             'modul_durak_id', 'durak_kume_id', 'peron_duragi', 'durak_id', 'ilcead', 'mahad',
                             'engellikullanim', 'engellirampa', 'uygunsuzluknedeni', 'o1', 'o2', 'o3', 'o4',
                             'durumu', 'sebebi', 'isletme_bolgesi', 'isletmealtbolgesi', 'durak_tipi',
                             'akilli_durak_durumu',
                             'abonelik_durumu', 'kaldirildi_mi', 'ikmal_noktasi_tipi', 'sofor_degisim_noktasi',
                             'cep_var', 'duraklama_durumu', 'fiziki_durum', 'elektirik_durumu', 'enerji_durumu',
                             'modul_durak_durumu', 'baslangic_durak_mi', 'hatkodu', 'hatadi'
                             ]
        for index, row in df.iterrows():
            for column in durak_all_columns:
                onceki, guncel = row[f"onceki_{column}"], row[f"guncel_{column}"]
                tarih = row["gdb_to_date"]

                if onceki != guncel:
                    result = {
                        'sutun_ismi': column,
                        'onceki': onceki,
                        'guncel': guncel,
                        'tarih': tarih
                    }
                    data.append(result)

        target = pd.DataFrame.from_records(data)

        # Saving
        output_folder = arcpy.env.scratchWorkspace
        if output_folder.endswith('.gdb'):
            output_folder = arcpy.env.scratchFolder

        out_job_path = os.path.join(output_folder, 'durak_degisim.xlsx')
        arcpy.AddMessage("excel output path : {0}".format(out_job_path))

        target.to_excel(out_job_path)

        arcpy.SetParameter(0, out_job_path)
        return