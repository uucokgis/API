from ..config import *

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


def coordinate_transform(row, src, trg):
    point = arcpy.Point(row[0], row[1])
    point_geom = arcpy.PointGeometry(point, src)
    projected_geom = point_geom.projectAs(trg)
    return projected_geom.firstPoint.X, projected_geom.firstPoint.Y


def df_project(df: pd.DataFrame, x, y, src: arcpy.SpatialReference, trg: arcpy.SpatialReference, drop_fields=True,
               new_column='TARGET'):
    # Use the swifter library to apply the function in parallel
    df[[f'{new_column}_X', f'{new_column}_Y']] = df.apply(lambda row: coordinate_transform(row[[x, y]], src, trg),
                                                                  axis=1, result_type='expand')
    if drop_fields:
        df.drop(columns=[x, y], inplace=True)

    return df
