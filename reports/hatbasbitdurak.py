from utils.datahelper import table_to_data_frame
from . import ITRF96_7932_PROJECTION
import pandas as pd
import pyproj
from ast import literal_eval

crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
crs_4326 = pyproj.CRS.from_epsg(4326)
transformer = pyproj.transformer.Transformer.from_crs(crs_7932, crs_4326, )


class HatBasBitDurak:
    hatbasbitdurak_df: pd.DataFrame

    @classmethod
    def get(cls):
        return cls.hatbasbitdurak_df

    @classmethod
    def fetch(cls):
        hat_columns = ['HAT_KODU', 'HAT_BASI', 'HAT_SONU', 'ISLETME_BOLGESI']
        durak_columns = ['DURAK_KODU', 'ISLETME_BOLGESI', 'SHAPE']

        hat_df: pd.DataFrame = table_to_data_frame('HAT', hat_columns)
        hat_df['SHAPE'] = hat_df['SHAPE'].apply(lambda x: transformer.transform(*literal_eval(x)))
        durak_df: pd.DataFrame = table_to_data_frame('DURAK', durak_columns, "DURUMU = 'AKTİF'")
        durak_df.rename(columns={'DURAK_KODU': 'HAT_BASI'}, inplace=True)

        bas_bit_hat_df = hat_df.join(durak_df[['SHAPE', 'HAT_BASI']], on='HAT_BASI', how='left')
        bas_bit_hat_df.rename(columns={'SHAPE': 'SHAPE_BASDURAK'}, inplace=True)

        durak_df.rename(columns={'HAT_BASI': 'HAT_SONU'}, inplace=True)
        bas_bit_hat_df = bas_bit_hat_df.join(durak_df[['SHAPE', 'HAT_SONU']], on='HAT_SONU', how='left')
        bas_bit_hat_df.rename(columns={'SHAPE': 'SHAPE_SONDURAK'}, inplace=True)

        return bas_bit_hat_df
