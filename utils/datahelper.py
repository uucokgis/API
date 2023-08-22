from itertools import product
from config import *

import pandas as pd


def table_to_data_frame(in_table, input_fields=None, where_clause=None, *convert_integers):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""
    try:
        if input_fields:
            final_fields = input_fields
        else:
            final_fields = [field.name for field in arcpy.ListFields(in_table)]

        data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]

        fc_dataframe = pd.DataFrame(data, columns=final_fields)

        if convert_integers:
            for col in convert_integers:
                fc_dataframe[col] = fc_dataframe[col].astype(int, errors='ignore')

        return fc_dataframe
    except OSError as err:
        arcpy.AddError("Veritabaninda {0} view'i bulunamadigi icin rapor uretilemedi. \n".format(in_table))
        arcpy.AddError("Hata : {0}".format(err))