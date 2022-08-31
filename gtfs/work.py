import os
from unittest import TestCase
import arcpy, sys, pandas as pd

guzergah_path = r"C:\\YAYIN\\PG\\sde_gyy.sde\\gyy.sde.VW_GTFS_GUZERGAH"
durak_path = r"C:\\YAYIN\\PG\\sde_gyy.sde\\gyy.sde.VW_GTFS_DURAK"


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

        sys.exit(0)


class TransformData(TestCase):
    def test_guzergah_gtfs(self):
        """
        route_id*, route_short_name*, route_long_name, route_desc, route_type*
        :return:
        """
        output = os.path.abspath("routes.txt")
        guzergah = table_to_data_frame(guzergah_path)

        with open(output, 'w') as writer:
            writer.write("route_id, route_short_name, route_long_name, route_desc, route_type \n")

            for index, row in guzergah.iterrows():
                data = str(row.tolist())[1:-1]
                writer.write(data)

        writer.close()

    def test_durak_gtfs(self):
        """
        stop_id*, stop_code, stop_name*, stop_desc, stop_lat*, stop_lon*,
        location_type
        :return:
        """
        output = os.path.abspath("stops.txt")
        durak = table_to_data_frame(durak_path)

        with open(output, 'w') as writer:
            writer.write("stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type \n")

            for index, row in durak.iterrows():
                data = str(row.tolist())[1:-1]
                writer.write(data)

        writer.close()
