from itertools import product

import pandas as pd

from ast import literal_eval
import time, os

from utils.RoadGenerator import RoadGenerator
from utils.datahelper import combinator
from yeniden import SDE_PATH, DB_SCHEMA
from yeniden.hatbasbitdurak import transformer


class BARapor:
    def __init__(self, hatbasbitdurak_df=None):
        self.hatbasbitdurak_df = hatbasbitdurak_df

    def initial(self):
        # initial settings
        ba_view_df = self.hatbasbitdurak_df.drop_duplicates(subset=['HAT_BASI', 'HAT_SONU'])
        ba_view_df = ba_view_df.head(10)
        ba_view_df['HAT_BASI'] = ba_view_df['HAT_BASI'].astype(int)
        ba_view_df['HAT_SONU'] = ba_view_df['HAT_SONU'].astype(int)
        ba_view_df.rename(columns={'SHAPE_HAT': 'SHAPE_BASDURAK'}, inplace=True)  # todo:
        ba_view_df['SHAPE_BASDURAK'] = ba_view_df['SHAPE_BASDURAK'].apply(
            lambda x: transformer.transform(*literal_eval(x)))
        ba_view_df['SHAPE_SONDURAK'] = ba_view_df['SHAPE_SONDURAK'].apply(
            lambda x: transformer.transform(*literal_eval(x)))

        return ba_view_df

    def generate(self):
        start_time = time.time()
        ba_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.BA_RAPOR")
        ba_df = self.initial()

        combinations = combinator(ba_df, 'HAT_BASI', 'HAT_SONU', 'SHAPE_BASDURAK', 'SHAPE_SONDURAK')
        rg = RoadGenerator(combinations, oid='index')
        # rg.df = rg.df.head(20)  # todo:
        # rg.concurrent_road_generator()
        # rg.road_to_gdf()

        # rg.df.spatial.to_featureclass(ba_report_out, overwrite=True)
        end_time = time.time()

        return f"Succeeded: {end_time - start_time} seconds"
