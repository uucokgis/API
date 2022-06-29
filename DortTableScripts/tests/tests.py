import time
from unittest import TestCase
from arcpy import env
import arcpy
import os
from DortTableScripts.RoadGenerator import RoadGenerator
from DurakGarajAraci import table_to_data_frame, network_service_uri

SDE_PATH = 'C:\\YAYIN\\PG\\sde_gyy.sde'
EXCEL_PATH = 'C:\\YAYIN\\PG\\WKT_EXCELS'

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

    @staticmethod
    def durak_garaj_rota(_type='BASLANGIC'):
        start_time = time.time()
        if _type == 'BASLANGIC':
            durak_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.view_durak_hb_garaj")
            durak_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhb_garaj_rota")
        else:  # BITIS
            durak_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.view_durak_hs_garaj")
            durak_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhs_garaj_rota")

        hbas_report_df = table_to_data_frame(durak_garaj_view)
        hbas_report_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "garaj_x": "to_x",
            "garaj_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(hbas_report_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(durak_report_out, overwrite=True)
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")
        assert arcpy.Exists(durak_report_out)

    def test_durak_garaj_rota_hb_hs(self):
        # hb ve hs
        start_time = time.time()
        self.durak_garaj_rota()
        self.durak_garaj_rota(_type='BITIS')
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")

    def test_durak_garaj_rota_hepsi(self):
        durak_garaj_all_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_DURAK_GARAJ_HEPSI")
        durak_garaj_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_GARAJ_HEPSI_ROTA")

        durak_garaj_df = table_to_data_frame(durak_garaj_all_view)
        durak_garaj_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "garaj_x": "to_x",
            "garaj_y": "to_y"
        }, inplace=True)

        rg = RoadGenerator(durak_garaj_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(durak_garaj_report_out, overwrite=True)
        assert arcpy.Exists(durak_garaj_report_out)

    @staticmethod
    def durak_gar_rota(_type='BASLANGIC'):
        start_time = time.time()
        if _type == 'BASLANGIC':
            durak_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.view_gar_hb")
            durak_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhb_gar_rota")
        else:  # BITIS
            durak_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.view_gar_hs")
            durak_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.durakhs_gar_rota")

        hbas_report_df = table_to_data_frame(durak_garaj_view)
        hbas_report_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "gar_x": "to_x",
            "gar_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(hbas_report_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(durak_report_out, overwrite=True)
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")
        assert arcpy.Exists(durak_report_out)

    def test_gar_durak_rota(self):
        start_time = time.time()
        self.durak_gar_rota()
        self.durak_gar_rota(_type='BITIS')
        end_time = time.time()
        print(f"Gecen zaman : {end_time - start_time} saniye")

    def test_gar_durak_all_rota(self):
        start_time = time.time()
        gar_durak_view_path = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_DURAK_GAR_HEPSI")
        gar_durak_output = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_GAR_HEPSI_ROTA")

        gar_durak_df = table_to_data_frame(gar_durak_view_path)
        gar_durak_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "gar_x": "to_x",
            "gar_y": "to_y"
        }, inplace=True)

        rg = RoadGenerator(gar_durak_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(gar_durak_output, overwrite=True)
        print(f"Gecen zaman : {time.time() - start_time}")

        assert arcpy.Exists(gar_durak_output)

    def test_garaj_garaj_rota(self):
        garaj_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_GARAJ_GARAJ")
        garaj_garaj_output = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_GARAJ_ROTA")
        # garaj_garaj_excel = os.path.join(EXCEL_PATH, 'GARAJ_GARAJ_ROTA.xlsx')

        gg_df = table_to_data_frame(garaj_garaj_view)
        gg_df.rename(columns={
            "bas_garaj_x": "from_x",
            "bas_garaj_y": "from_y",
            "bit_garaj_x": "to_x",
            "bit_garaj_y": "to_y"
        }, inplace=True)
        rg = RoadGenerator(gg_df, oid='row_id')
        rg.concurrent_road_generator()
        # gg_wkt = rg.road_to_wkt()
        # gg_wkt.to_excel(os.path.join(EXCEL_PATH, 'GarajGarajWKT.xlsx'))
        rg.road_to_gdf()

        rg.df.spatial.to_featureclass(garaj_garaj_output, overwrite=True)
        assert arcpy.Exists(garaj_garaj_output)
