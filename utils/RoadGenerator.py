import concurrent.futures
import time

import arcpy
import geopandas as gpd
import pandas as pd
import requests
from arcgis.features import GeoAccessor
from arcpy import AddWarning as wrn
from shapely.geometry import LineString

from config import *


class RoadGenerator:
    COLUMNS = {"FROM_X", "FROM_Y", "TO_X", "TO_Y"}

    def __init__(self, df: pd.DataFrame, oid, spt_ref=arcpy.SpatialReference(4326)):
        self.spt_ref = spt_ref
        self.oid = oid
        self.df = df
        self.check_columns()
        self.prepare_urls()

    def check_columns(self):
        cols = self.df.columns
        for c in self.COLUMNS:
            if c not in cols:
                raise ValueError(f"Check columns: {c}")

    def prepare_urls(self):
        self.df['URL'] = self.df[self.COLUMNS].apply(
            lambda x: network_service_uri.format(bas_x=x.FROM_X, bas_y=x.FROM_Y, bit_x=x.TO_X, bit_y=x.TO_Y,
                                                 ara=""), axis=1)

    @staticmethod
    def get_route(url, oid, return_arcpy=False, spt_ref=arcpy.SpatialReference(4326)):
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
            if return_arcpy:
                line_geom = arcpy.Polyline(arcpy.Array([arcpy.PointGeometry(arcpy.Point(*i), spt_ref) for i in resp_coords]))
            else:
                line_geom = LineString(resp_coords)
            return line_geom, mesafe, sure, oid

        except Exception as err:
            wrn(f"cbsproxy error : {str(err)} - {5}")

    def concurrent_road_generator(self):
        start_time = time.time()
        values = [i for _, i in self.df[[self.oid, 'URL']].iterrows()]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_route, url=row.URL, oid=row[self.oid]) for row in values
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

            results = pd.DataFrame(results, columns=['SHAPE', 'mesafe', 'sure', self.oid])
            print(f"Result are collected : {time.time() - start_time} seconds")

            self.df = pd.merge(self.df.reset_index(drop=True), results)

    def road_to_gdf(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='SHAPE', crs='epsg:4326')
        gdf = GeoAccessor.from_geodataframe(gdf)
        self.df = gdf
