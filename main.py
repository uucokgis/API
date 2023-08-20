from flask import Flask
from yeniden.ba_rapor import BARapor
from yeniden.durak_gar import DurakGar
from yeniden.durak_garaj import DurakGaraj
from yeniden.garaj_garaj import GarajGaraj
from yeniden.hatbasbitdurak import HatBasBitDurak
from yeniden.tests import ReportTests

app = Flask(__name__)


@app.route("/reports/generate/ba")
def ba():
    # df = ReportTests.mock_hatbasbitdurak()  # todo
    hb = HatBasBitDurak()
    df = hb.fetch()
    ba_rapor = BARapor(df.hatbasbitdurak_df)
    result = ba_rapor.generate()
    return f"BA Report: {result}"


@app.route("/reports/generate/durak-garaj")
def durak_garaj():
    durakgaraj = DurakGaraj()
    durakgaraj.fetch()
    return "<p>Hello, World!</p>"


@app.route("/reports/generate/durak-gar")
def durak_gar():
    durakgar = DurakGar()
    durakgar.fetch()


@app.route("/reports/generate/garaj-garaj")
def garaj_garaj():
    garajgaraj = GarajGaraj()
    garajgaraj.fetch()


app.run(debug=True)
