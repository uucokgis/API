import concurrent.futures
import time

import geopandas as gpd
import pandas as pd
import requests
from arcgis.features import GeoAccessor
from arcpy import AddWarning as wrn
from shapely.geometry import LineString

from config import network_service_uri


class RoadGenerator:
    COLUMNS = {"FROM_X", "FROM_Y", "TO_X", "TO_Y"}

    def __init__(self, df: pd.DataFrame, oid):
        self.oid = oid
        self.df = df
        self.check_columns()
        self.prepare_uris()

    def check_columns(self):
        cols = self.df.columns
        for c in self.COLUMNS:
            if c not in cols:
                raise ValueError(f"Check columns: {c}")

    def prepare_uris(self):
        self.df['uris'] = None
        for ind, row in self.df.iterrows():
            bas_x, bas_y, bit_x, bit_y = row['FROM_X'], row['FROM_Y'], row['TO_X'], row['TO_Y']
            request_uri = network_service_uri.format(bas_x=bas_x, bas_y=bas_y,
                                                     bit_x=bit_x, bit_y=bit_y, ara="")
            self.df.at[ind, 'uris'] = request_uri

    @staticmethod
    def get_route(url, oid):
        try:
            resp = requests.get(url)
            data = resp.json()

            data = str(data['string']['#text'])

            resp_coords, direction = data.split(",@<table cellspacing='0'")
            resp_coords = resp_coords.split(",")
            mesafe_start = direction.find('<b>Mesafe : </b>')
            mesafe_end = direction.find(' km</td>')
            mesafe = direction[mesafe_start + 16: mesafe_end].replace(',', '.')
            mesafe = float(mesafe)

            sure_start = direction.find('<b>Süre : </b>')
            sure_end = direction.find(' dk</td>')
            sure = direction[sure_start + 14: sure_end].replace(',', '.')
            sure = float(sure)

            resp_coords = [i.split(' ') for i in resp_coords]
            resp_coords = [(float(i[0]), float(i[1])) for i in resp_coords]
            line_feature = LineString(resp_coords)
            return line_feature, mesafe, sure, oid

        except Exception as err:
            wrn(f"cbsproxy error : {str(err)} - {oid}")

    def concurrent_road_generator(self):
        start_time = time.time()
        values = [i for _, i in self.df[[self.oid, 'uris']].iterrows()]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_route, url=row.uris, oid=row[self.oid]) for row in values
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

            results = pd.DataFrame(results, columns=['geometry', 'mesafe', 'sure', self.oid])
            print(f"Result are collected : {time.time() - start_time} seconds")

            self.df = pd.merge(self.df.reset_index(drop=True), results)

    def road_to_wkt(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='geometry')
        return gdf.to_wkt()

    def road_to_gdf(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='geometry')
        gdf = GeoAccessor.from_geodataframe(gdf)
        self.df = gdf
