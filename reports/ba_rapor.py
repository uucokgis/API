import time
from config import *
from utils.RoadGenerator import RoadGenerator


class BARapor:
    ba_report_out = os.path.join(arcpy.env.workspace, f"{DB_SCHEMA}.BA_RAPOR")

    def __init__(self, hatbasbitdurak_df=None):
        self.hatbasbitdurak_df = hatbasbitdurak_df

    def generate(self):
        start_time = time.time()
        self.hatbasbitdurak_df.rename(columns={'SHAPE_BASDURAK_X': 'FROM_X', 'SHAPE_BASDURAK_Y': 'FROM_Y',
                                               'SHAPE_SONDURAK_X': 'TO_X', 'SHAPE_SONDURAK_Y': 'TO_Y'}, inplace=True)
        rg = RoadGenerator(self.hatbasbitdurak_df, oid='index')
        # rg.concurrent_road_generator()
        # rg.road_to_gdf()

        # rg.df.spatial.to_featureclass(ba_report_out, overwrite=True)
        end_time = time.time()

        return f"Succeeded: {end_time - start_time} seconds"
