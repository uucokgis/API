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

    def test_durak_garaj_rota_hepsi(self):
        durak_garaj_all_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_DURAK_GARAJ_HEPSI")
        durak_garaj_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_GARAJ_HEPSI_ROTA")
        garaj_durak_report_out = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_DURAK_HEPSI_ROTA")
        # durak -> garaj
        view_df = table_to_data_frame(durak_garaj_all_view)
        durak_garaj_df = view_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "garaj_x": "to_x",
            "garaj_y": "to_y"
        })
        garaj_durak_df = view_df.rename(columns={
            "garaj_x": "from_x",
            "garaj_y": "from_y",
            "durak_x": "to_x",
            "durak_y": "to_y"
        })
        rdg = RoadGenerator(durak_garaj_df, oid='row_id')
        rgd = RoadGenerator(garaj_durak_df, oid='row_id')

        rdg.concurrent_road_generator()
        rdg.road_to_gdf()

        rdg.df.spatial.to_featureclass(durak_garaj_report_out, overwrite=True)
        assert arcpy.Exists(durak_garaj_report_out)

        # tersi: garaj -> durak
        rgd.concurrent_road_generator()
        rgd.road_to_gdf()

        rgd.df.spatial.to_featureclass(garaj_durak_report_out, overwrite=True)
        assert arcpy.Exists(durak_garaj_report_out)

    def test_gar_durak_all_rota(self):
        start_time = time.time()
        view_path = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_DURAK_GAR_HEPSI")
        durak_gar_output = os.path.join(SDE_PATH, f"{DB_SCHEMA}.DURAK_GAR_ROTA")
        gar_durak_output = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GAR_DURAK_ROTA")

        view_df = table_to_data_frame(view_path)
        durak_gar_df = view_df.rename(columns={
            "durak_x": "from_x",
            "durak_y": "from_y",
            "gar_x": "to_x",
            "gar_y": "to_y"
        })
        gar_durak_df = view_df.rename(columns={
            "gar_x": "from_x",
            "gar_y": "from_y",
            "durak_x": "to_x",
            "durak_y": "to_y"
        })
        rdg = RoadGenerator(durak_gar_df, oid='row_id')
        rdg.concurrent_road_generator()
        rdg.road_to_gdf()

        rdg.df.spatial.to_featureclass(durak_gar_output, overwrite=True)
        assert arcpy.Exists(durak_gar_output)

        rgd = RoadGenerator(gar_durak_df, oid='row_id')
        rgd.concurrent_road_generator()
        rgd.road_to_gdf()

        rgd.df.spatial.to_featureclass(gar_durak_output, overwrite=True)
        print(f"Gecen zaman : {time.time() - start_time}")

        assert arcpy.Exists(gar_durak_output)

    def test_garaj_garaj_rota(self):
        garaj_garaj_view = os.path.join(SDE_PATH, f"{DB_SCHEMA}.VIEW_GARAJ_GARAJ")
        garaj_garaj_output = os.path.join(SDE_PATH, f"{DB_SCHEMA}.GARAJ_GARAJ_ROTA")

        view_df = table_to_data_frame(garaj_garaj_view)
        gg_df = view_df.rename(columns={
            "bas_garaj_x": "from_x",
            "bas_garaj_y": "from_y",
            "bit_garaj_x": "to_x",
            "bit_garaj_y": "to_y"
        })
        gg_df_rev = view_df.rename(columns={
            "bas_garaj_x": "to_x",
            "bas_garaj_y": "to_y",
            "bit_garaj_x": "from_x",
            "bit_garaj_y": "from_y"
        })

        rg = RoadGenerator(gg_df, oid='row_id')
        rg.concurrent_road_generator()
        rg.road_to_gdf()

        # rg.df.spatial.to_featureclass(garaj_garaj_output, overwrite=True)
        # assert arcpy.Exists(garaj_garaj_output)

        rg_rev = RoadGenerator(gg_df_rev, oid='row_id')
        rg_rev.concurrent_road_generator()
        rg_rev.road_to_gdf()

        # rg.df.spatial.to_featureclass(garaj_garaj_output, overwrite=True)
        # assert arcpy.Exists(garaj_garaj_output)

        # merge
        df_merged = rg.df.append(rg_rev.df, ignore_index=True)

        df_merged.spatial.to_featureclass(garaj_garaj_output, overwrite=True)