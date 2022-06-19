import time
from unittest import TestCase
from arcpy import env
import arcpy
import os
from DortTableScripts.RoadGenerator import RoadGenerator
from DurakGarajAraci import table_to_data_frame, network_service_uri

SDE_PATH = 'C:\\YAYIN\\PG\\sde_gyy.sde'
DB_SCHEMA = "gyy.sde"

env.workspace = SDE_PATH


class DortTableTests(TestCase):
    def test_ba_raporu(self):
        start_time = time.time()
        ba_report_view = f"{DB_SCHEMA}.VIEW_BA_RAPOR"
        ba_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.BA_RAPOR")
        ba_report_df = table_to_data_frame(ba_report_view)
        ba_report_df.rename(columns={
            "bas_durak_x": "from_x",
            "bas_durak_y": "from_y",
            "bit_durak_x": "to_x",
            "bit_durak_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(ba_report_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(ba_report_out, overwrite=True)
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")
        assert arcpy.Exists(ba_report_out)

    def test_durak_baslangic_garaj_rota(self):
        start_time = time.time()
        hbas_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.view_durak_hs_garaj")
        hbas_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhb_garaj_rota")
        hbas_report_df = table_to_data_frame(hbas_garaj_view)
        hbas_report_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "garaj_x": "to_x",
            "garaj_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(hbas_report_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(hbas_report_out, overwrite=True)
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")
        assert arcpy.Exists(hbas_report_out)

    def test_durak_bitis_garaj_rota(self):
        start_time = time.time()
        hbit_garaj_view = f"{DB_SCHEMA}.durakhs_garaj_view"
        hbit_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhs_garaj_rota")
        hbit_report_df = table_to_data_frame(hbit_garaj_view)
        hbit_report_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "garaj_x": "to_x",
            "garaj_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(hbit_report_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(hbit_report_out, overwrite=True)
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")
        assert arcpy.Exists(hbit_report_out)

    def test_gar_durak_rota(self):
        raise NotImplementedError

    def test_garaj_garaj_rota(self):
        raise NotImplementedError
