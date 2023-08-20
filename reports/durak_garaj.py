from utils.RoadGenerator import RoadGenerator
from utils.datahelper import table_to_data_frame, combinator
import pandas as pd


class DurakGaraj:
    def fetch(self):
        durak_columns = ['DURAK_KODU', 'ISLETME_BOLGESI', 'SHAPE']
        garaj_columns = ['GARAJ_KODU', 'ISLETME_BOLGESI', 'SHAPE']
        anadolu_isletme_bolgeleri = """ISLETME_BOLGESI IN (1,2)"""
        avrupa_isletme_bolgeleri = """ISLETME_BOLGESI IN (3,4,5)"""

        durak_anadolu: pd.DataFrame = table_to_data_frame('DURAK', durak_columns, anadolu_isletme_bolgeleri)
        garaj_anadolu: pd.DataFrame = table_to_data_frame('GARAJ', garaj_columns, anadolu_isletme_bolgeleri)

        durak_avrupa: pd.DataFrame = table_to_data_frame('DURAK', durak_columns, avrupa_isletme_bolgeleri)
        garaj_avrupa: pd.DataFrame = table_to_data_frame('GARAJ', garaj_columns, avrupa_isletme_bolgeleri)

        # anadolu
        anadolu_combinations = set()
        for _, durak in durak_anadolu.iterrows():
            for _, garaj in garaj_anadolu.iterrows():
                anadolu_combinations.add((durak.DURAK_KODU, garaj.GARAJ_KODU, durak.SHAPE, garaj.SHAPE))
                # todo: no need
                # anadolu_combinations.add((garaj.GARAJ_KODU, durak.DURAK_KODU, garaj.SHAPE, durak.SHAPE))

        anadolu_combinations = pd.DataFrame(anadolu_combinations,
                                            columns=['DURAK_KODU', 'GARAJ_KODU', 'DURAK_SHAPE', 'GARAJ_SHAPE'])
        anadolu_combinations.reset_index(inplace=True)
        rg = RoadGenerator(anadolu_combinations, 'index')

        rg.df = rg.df.head(20)  # todo
        # rg.concurrent_road_generator()
        # rg.road_to_gdf()
