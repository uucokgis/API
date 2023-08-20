import os
import time

from config import DB_SCHEMA, SDE_PATH
from utils.RoadGenerator import RoadGenerator
from utils.datahelper import table_to_data_frame


def get_view():
    query = """select att.hatbitdurak, att.hatbasdurak, att.BASSHAPE, att.BITSHAPE,
           att.db_isletme_bolgesi, att.ds_isletme_bolgesi,
                  (row_number() OVER (ORDER BY att.hatbasdurak))::integer AS row_id
                   from(select distinct hv2.hatbitdurak, 
                   hv.hatbasdurak, hv.bas_durak_x, hv.bas_durak_y,
                   hv2.bit_durak_x, hv2.bit_durak_y, hv.db_isletme_bolgesi, 
                   hv2.ds_isletme_bolgesi from VIEW_HATBASBITDURAK hv, 
                   VIEW_HATBASBITDURAK hv2where hv.hatbasdurak != hv2.hatbitdurak and hv.db_isletme_bolgesi in (1,2) and 
                   hv2.ds_isletme_bolgesi in (1,2)or hv.db_isletme_bolgesi in (3,4,5) AND hv2.ds_isletme_bolgesi IN (3,4,5) 
                   order by hv2.hatbitdurak) as att;
    """


def generate_ba():
    start_time = time.time()
    ba_report_view = f"{DB_SCHEMA}.VIEW_BA_RAPOR"
    ba_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.BA_RAPOR")
    ba_report_df = table_to_data_frame(ba_report_view)
    rg = RoadGenerator(ba_report_df, oid='row_id')
    rg.concurrent_road_generator()
    rg.road_to_gdf()

    rg.df.spatial.to_featureclass(ba_report_out, overwrite=True)
    end_time = time.time()

    return ba_report_out
