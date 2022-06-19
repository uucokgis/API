import concurrent.futures
from concurrent.futures import ALL_COMPLETED

import aiohttp
import pandas as pd
import geopandas as gpd
from arcgis.features import GeoAccessor
import requests
from shapely.geometry import LineString
from arcpy import AddWarning as wrn

network_service_uri = "https://cbsproxy.ibb.gov.tr/?networkws&baslangic={bas_x}%7C{bas_y}" \
                      "&ara={ara}" \
                      "&bitis={bit_x}%7C{bit_y}"


class RoadGenerator:
    COLUMNS = {"from_x", "from_y", "to_x", "to_y"}

    def __init__(self, df: pd.DataFrame, oid='rowid'):
        self.oid = oid
        self.df = df
        # testing
        self.df = self.df.head(10)
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
            mesafe_end = direction.find(' m<br></td>')
            mesafe = direction[mesafe_start + 16: mesafe_end].replace(',', '.')
            mesafe = float(mesafe)

            resp_coords = [i.split(' ') for i in resp_coords]
            resp_coords = [(float(i[0]), float(i[1])) for i in resp_coords]
            line_feature = LineString(resp_coords)
            return line_feature, mesafe, oid

        except Exception as err:
            wrn(f"cbsproxy error : {str(err)} - {oid}")

    def concurrent_road_generator(self):
        values = [i for _, i in self.df[[self.oid, 'uris']].iterrows()]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_route, url=row.uris, oid=row.row_id) for row in values
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

            results = pd.DataFrame(results, columns=['geometry', 'mesafe', self.oid])

            self.df = pd.merge(self.df.reset_index(drop=True), results)

    def road_to_gdf(self):
        gdf = gpd.GeoDataFrame(self.df, geometry='geometry')
        gdf = GeoAccessor.from_geodataframe(gdf)
        self.df = gdf

