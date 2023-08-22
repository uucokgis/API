from itertools import product

from utils.datahelper import table_to_data_frame
from config import *
import pandas as pd
import pyproj

crs_7932 = pyproj.CRS.from_user_input(ITRF96_7932_PROJECTION)
crs_4326 = pyproj.CRS.from_epsg(4326)
transformer = pyproj.transformer.Transformer.from_crs(crs_7932, crs_4326, )


class HatBasBitDurak:
    hatbasbitdurak_df: pd.DataFrame
    hat_columns = ['HAT_KODU', 'HAT_BASI', 'HAT_SONU']
    durak_columns = ['DURAK_KODU', 'SHAPE']

    @classmethod
    def get_bolgeler(cls, bolge='ANADOLU', text_return=True):  # ANADOLU, AVRUPA
        if bolge == 'ANADOLU':
            if text_return:
                return 'ANADOLU1', 'ANADOLU2'
            else:
                return 1,2
        elif bolge == 'AVRUPA':
            if text_return:
                return 'AVRUPA1', 'AVRUPA2', 'AVRUPA3'
            else:
                return 3,4,5

    @classmethod
    def _fetch(cls, ana_bolge='ANADOLU'):
        hat_df = table_to_data_frame('HAT', cls.hat_columns, f"ISLETME_BOLGESI IN "
                                                             f"{tuple(cls.get_bolgeler(ana_bolge, False))}")
        hat_df.dropna(subset=['HAT_BASI', 'HAT_SONU'], inplace=True)
        hat_df.drop_duplicates(subset=['HAT_BASI', 'HAT_SONU'], inplace=True)
        hat_df = hat_df.query("HAT_SONU != 0 and HAT_SONU != 0")
        hat_df['HAT_BASI'], hat_df['HAT_SONU'], = hat_df['HAT_BASI'].astype(int), hat_df['HAT_SONU'].astype(int)

        durak_df = pd.concat([table_to_data_frame(f'{bolge}_DURAK', cls.durak_columns) for bolge in cls.get_bolgeler(ana_bolge)])
        durak_df['DURAK_KODU'] = durak_df['DURAK_KODU'].astype(int)
        durak_df.drop_duplicates(subset=['DURAK_KODU'], inplace=True)
        durak_df.set_index('DURAK_KODU', inplace=True)

        combinations_hat_df = pd.DataFrame(set(product(hat_df['HAT_BASI'], hat_df['HAT_SONU'])),
                                           columns=['HAT_BASI', 'HAT_SONU'])

        bas_bit_hat_df = combinations_hat_df.set_index('HAT_BASI', drop=False)
        bas_bit_hat_df = bas_bit_hat_df.join(durak_df, lsuffix='_x')
        bas_bit_hat_df.rename(columns={'SHAPE': 'SHAPE_BASDURAK'}, inplace=True)
        bas_bit_hat_df = bas_bit_hat_df.set_index('HAT_SONU', drop=False)
        bas_bit_hat_df = bas_bit_hat_df.join(durak_df, lsuffix='_y')
        bas_bit_hat_df.rename(columns={'SHAPE': 'SHAPE_SONDURAK'}, inplace=True)
        bas_bit_hat_df.reset_index(inplace=True)
        bas_bit_hat_df.dropna(subset=['SHAPE_BASDURAK', 'SHAPE_SONDURAK'], inplace=True)

        bas_bit_hat_df['SHAPE_BASDURAK_X'], bas_bit_hat_df['SHAPE_BASDURAK_Y'] = zip(*bas_bit_hat_df['SHAPE_BASDURAK'])
        bas_bit_hat_df['SHAPE_SONDURAK_X'], bas_bit_hat_df['SHAPE_SONDURAK_Y'] = zip(*bas_bit_hat_df['SHAPE_SONDURAK'])

        bas_bit_hat_df.drop(columns=['SHAPE_BASDURAK', 'SHAPE_SONDURAK'], inplace=True)
        cls.hatbasbitdurak_df = bas_bit_hat_df
        return bas_bit_hat_df
