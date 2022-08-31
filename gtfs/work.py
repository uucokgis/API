import os.path
from unittest import TestCase

import pandas as pd

from gtfs import table_to_data_frame
guzergah_path = r"C:\\YAYIN\\PG\\sde_gyy.sde\\gyy.sde.VW_GTFS_GUZERGAH"
durak_path = r"C:\\YAYIN\\PG\\sde_gyy.sde\\gyy.sde.VW_GTFS_DURAK"


class TransformData(TestCase):
    def test_guzergah_gtfs(self):
        """
        route_id*, route_short_name*, route_long_name, route_desc, route_type*
        :return:
        """
        output =  os.path.abspath("routes.txt")
        guzergah = table_to_data_frame(guzergah_path)

        with open(output, 'w') as writer:
            writer.write("route_id, route_short_name, route_long_name, route_desc, route_type \n")

            for index, row in guzergah.iterrows():
                data = row

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
                data = row