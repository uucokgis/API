import os
import pandas as pd
from unittest import TestCase

from reports.ba_rapor import BARapor
from reports.durak_gar import DurakGar
from reports.durak_garaj import DurakGaraj
from reports.garaj_garaj import GarajGaraj
from reports.hatbasbitdurak import HatBasBitDurak


class ReportTests(TestCase):
    @staticmethod
    def mock_hatbasbitdurak():
        hatbasbitdurak = os.path.join('map', 'readydata', 'hatbasbitdurak.csv')
        df = pd.read_csv(hatbasbitdurak)
        df.rename(columns={'Unnamed: 0': 'OID'}, inplace=True)
        HatBasBitDurak.hatbasbitdurak_df = df
        print("mock data has been set")
        return HatBasBitDurak

    # todo: only for testing
    # def setUp(self) -> None:
    #     self.mock_hatbasbitdurak()

    def test_ba_rapor(self):
        df = HatBasBitDurak._fetch()
        df = df.head(20)  # todo: test
        ba_rapor = BARapor(df)
        ba_rapor.generate()
        print("BA is generated")

    def test_durak_garaj(self):
        durak_garaj = DurakGaraj()
        durak_garaj.fetch()

    def test_durak_gar(self):
        ba_rapor = DurakGar()
        ba_rapor.fetch()

    def test_garaj_garaj(self):
        durak_garaj = GarajGaraj()
        durak_garaj.fetch()
