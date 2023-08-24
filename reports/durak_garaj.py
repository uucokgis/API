from ..utils.RoadGenerator import RoadGenerator
from ..utils.datahelper import table_to_data_frame
import pandas as pd


class DurakGaraj:
    def fetch(self):
        durak_columns = ['DURAK_KODU', 'ISLETME_BOLGESI', 'SHAPE']
        garaj_columns = ['GARAJ_KODU', 'ISLETME_BOLGESI', 'GEOLOC']
        anadolu_isletme_bolgeleri = """ISLETME_BOLGESI IN ('ANADOLU1', 'ANADOLU2')"""
        g_anadolu_isletme_bolgeleri = """ISLETME_BOLGESI IN (1,2)"""
        avrupa_isletme_bolgeleri = """ISLETME_BOLGESI IN ('AVRUPA1','AVRUPA2','AVRUPA3')"""
        g_avrupa_isletme_bolgeleri = """ISLETME_BOLGESI IN (3,4,5)"""

        durak_anadolu: pd.DataFrame = table_to_data_frame('DURAK', durak_columns, anadolu_isletme_bolgeleri)
        garaj_anadolu: pd.DataFrame = table_to_data_frame('GARAJ', garaj_columns, g_anadolu_isletme_bolgeleri)

        durak_avrupa: pd.DataFrame = table_to_data_frame('DURAK', durak_columns, avrupa_isletme_bolgeleri)
        garaj_avrupa: pd.DataFrame = table_to_data_frame('GARAJ', garaj_columns, g_avrupa_isletme_bolgeleri)

        # anadolu
        anadolu_combinations = set()
        for _, durak in durak_anadolu.iterrows():
            for _, garaj in garaj_anadolu.iterrows():
                anadolu_combinations.add((durak.DURAK_KODU, garaj.GARAJ_KODU, durak.SHAPE, garaj.GEOLOC))

        anadolu_combinations = pd.DataFrame(anadolu_combinations,
                                            columns=['DURAK_KODU', 'GARAJ_KODU', 'DURAK_SHAPE', 'GARAJ_SHAPE'])
        anadolu_combinations.reset_index(inplace=True)
        rg = RoadGenerator(anadolu_combinations, 'index')

        rg.df = rg.df.head(20)  # todo
        # rg.concurrent_road_generator()
        # rg.road_to_gdf()


        # avrupa
        avrupa_combinations = set()
        for _, durak in durak_avrupa.iterrows():
            for _, garaj in garaj_avrupa.iterrows():
                avrupa_combinations.add((durak.DURAK_KODU, garaj.GARAJ_KODU, durak.SHAPE, garaj.GEOLOC))

        avrupa_combinations = pd.DataFrame(avrupa_combinations,
                                            columns=['DURAK_KODU', 'GARAJ_KODU', 'DURAK_SHAPE', 'GARAJ_SHAPE'])
