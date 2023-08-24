import time
from ..config import *
from ..utils.RoadGenerator import RoadGenerator


class BARapor:
    ba_report_out = os.path.join(arcpy.env.workspace, f"{DB_SCHEMA}.BA_RAPOR")

    def __init__(self, hatbasbitdurak_df=None):
        self.hatbasbitdurak_df = hatbasbitdurak_df

    def generate(self, out_id):
        start_time = time.time()
        self.hatbasbitdurak_df.rename(columns={'BASDURAK_X': 'FROM_X', 'BASDURAK_Y': 'FROM_Y',
                                               'SONDURAK_X': 'TO_X', 'SONDURAK_Y': 'TO_Y'}, inplace=True)
        rg = RoadGenerator(self.hatbasbitdurak_df, oid='index')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        report_out = f"{self.ba_report_out}_{out_id}"
        rg.df = rg.df.drop(columns=['FROM_X', 'FROM_Y', 'TO_X', 'TO_Y', 'URL'])
        rg.df.spatial.to_featureclass(report_out, overwrite=True)
        end_time = time.time()

        return f"Succeeded: {end_time - start_time} seconds \n" \
               f"{report_out}"
