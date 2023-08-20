import arcpy
import pandas as pd


sde_prod = r"C:\YAYIN\TESTS\AKTARIM\New Folder\IETTPROD.sde"
sde_test = r"C:\YAYIN\TESTS\AKTARIM\New Folder\IETTORIGIN - SDE.sde"

arcpy.env.workspace = sde_prod


def table_to_data_frame(in_table, input_fields=None, where_clause=None):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""
    try:
        if input_fields:
            final_fields = input_fields
        else:
            final_fields = [field.name for field in arcpy.ListFields(in_table)]

        data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]

        fc_dataframe = pd.DataFrame(data, columns=final_fields)

        return fc_dataframe
    except OSError as err:
        arcpy.AddError("Veritabaninda {0} view'i bulunamadigi icin rapor uretilemedi. \n".format(in_table))
        arcpy.AddError("Hata : {0}".format(err))