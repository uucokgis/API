import concurrent.futures
import time
from concurrent.futures import ALL_COMPLETED

import aiohttp
import pandas as pd
import geopandas as gpd
from arcgis.features import GeoAccessor
import requests
from shapely.geometry import LineString
from arcpy import AddWarning as wrn
import arcpy
import pyproj

network_service_uri = "https://cbsproxy.ibb.gov.tr/?networkws&baslangic={bas_x}%7C{bas_y}" \
                      "&ara={ara}" \
                      "&bitis={bit_x}%7C{bit_y}"
ITRF96_7932_PROJECTION = """PROJCS["ITRF96 / TM30",GEOGCS["GCS_ITRF_1996",DATUM["D_ITRF_1996",
SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],
PARAMETER["central_meridian",30.0],PARAMETER["scale_factor",1.0],PARAMETER["latitude_of_origin",0.0],
UNIT["m",1.0]]"""
crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)


class RoadGenerator:
    COLUMNS = {"from_x", "from_y", "to_x", "to_y"}

    def __init__(self, df: pd.DataFrame, oid='rowid'):
        self.oid = oid
        self.df = df
        # testing
        self.df = self.df.head(10) # filter: hat basi hat sonu karisik al
        self.check_columns()
        self.prepare_uris()

    def check_columns(self):
        cols = self.df.columns
        for c in self.COLUMNS:
            if c not in cols:
                raise ValueError("Check columns !")

    def prepare_uris(self):
        self.df['uris'] = None
        for ind, row in self.df.iterrows():
            bas_x, bas_y, bit_x, bit_y = row['from_x'], row['from_y'], row['to_x'], row['to_y']
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
            mesafe_end = direction.find(' km<br></td>')
            mesafe = direction[mesafe_start + 16: mesafe_end].replace(',', '.')
            mesafe = float(mesafe)

            resp_coords = [i.split(' ') for i in resp_coords]
            resp_coords = [(float(i[0]), float(i[1])) for i in resp_coords]
            line_feature = LineString(resp_coords)
            return line_feature, mesafe, oid

        except Exception as err:
            wrn(f"cbsproxy error : {str(err)} - {oid}")

    def concurrent_road_generator(self):
        start_time = time.time()
        values = [i for _, i in self.df[[self.oid, 'uris']].iterrows()]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_route, url=row.uris, oid=row.row_id) for row in values
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

            results = pd.DataFrame(results, columns=['geometry', 'mesafe', self.oid])
            print(f"Result are collected : {time.time() - start_time} seconds")

            self.df = pd.merge(self.df.reset_index(drop=True), results)

    def road_to_wkt(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='geometry')
        return gdf.to_wkt()

    def road_to_gdf(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='geometry')
        gdf = GeoAccessor.from_geodataframe(gdf)
        self.df = gdf
