from unittest import TestCase

from yeniden.durak_garaj import DurakGaraj
from yeniden.hatbasbitdurak import HatBasBitDurak
from yeniden.ba_rapor import BARapor
import os, pandas as pd


class ReportTests(TestCase):
    @staticmethod
    def mock_hatbasbitdurak():
        hatbasbitdurak = os.path.join(os.path.abspath('.'), 'yeniden', 'reports', 'hatbasbitdurak.csv')
        df = pd.read_csv(hatbasbitdurak)
        df.rename(columns={'Unnamed: 0': 'OID'}, inplace=True)
        HatBasBitDurak.hatbasbitdurak_df = df
        print("mock data has been set")
        return HatBasBitDurak

    def setUp(self) -> None:
        self.mock_hatbasbitdurak()

    def test_ba_rapor(self):
        ba_rapor = BARapor(HatBasBitDurak.get())
        ba_rapor.generate()

    def test_durak_garaj(self):
        durak_garaj = DurakGaraj()
        durak_garaj.fetch()
