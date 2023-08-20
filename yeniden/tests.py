import os
import pandas as pd
from unittest import TestCase

from yeniden.ba_rapor import BARapor
from yeniden.durak_gar import DurakGar
from yeniden.durak_garaj import DurakGaraj
from yeniden.garaj_garaj import GarajGaraj
from yeniden.hatbasbitdurak import HatBasBitDurak


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

    def test_durak_gar(self):
        ba_rapor = DurakGar()
        ba_rapor.fetch()

    def test_garaj_garaj(self):
        durak_garaj = GarajGaraj()
        durak_garaj.fetch()
