import os.path
from unittest import TestCase

import pandas as pd

from gtfs import table_to_data_frame, guzergah_path, hat_path, durak_path


class GenerateTrips(TestCase):
    def test_create_trips(self):
        trip_output = os.path.abspath("trips.txt")

        gdf = table_to_data_frame(guzergah_path)
        with open(trip_output, 'w') as writer:
            writer.write('route_id, service_id, trip_id \n')
            for index, row in gdf.iterrows():
                text = "{0}, mon-tues-wed-thurs-fri-sat-sun, trip_{1} \n".format(int(row.guzergah_id), index)
                writer.write(text)

        writer.close()
        print("writing is OK")

    def test_create_stop_times(self):
        stop_times_columns = ['trip_id', 'arrival_time', 'departure_time', 'stop_id']

        stop_times_output = os.path.abspath("stop_times.txt")
        gdf = table_to_data_frame(hat_path)
        with open(stop_times_output, 'w') as writer:
            # todo:
            writer.write("trip_id, arrival_time, departure_time, stop_id \n")

            for index, row in gdf.iterrows():
                pass

    def test_create_routes(self):
        # route_type : 3: bus
        routes_columns = ['route_id', 'agency_id', 'route_short_name', 'route_long_name',
                          'route_desc', 'route_type']
        routes_output = os.path.abspath("routes.txt")

        gdf = table_to_data_frame(guzergah_path)
        with open(routes_output, 'w') as writer:
            writer.write("route_id, agency_id, route_short_name, route_long_name,route_desc, route_type \n")
            for index, row in gdf.iterrows():
                # todo:
                pass


class TransformData(TestCase):
    def test_guzergah_gtfs(self):
        pass

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
                data = row['durak_kodu']