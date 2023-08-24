from flask import Flask
from reports.ba_rapor import BARapor
from reports.durak_gar import DurakGar
from reports.durak_garaj import DurakGaraj
from reports.garaj_garaj import GarajGaraj
from reports.hatbasbitdurak import HatBasBitDurak
from config import *

app = Flask(__name__)


@app.route("/reports/generate/ba", methods=['GET', 'POST'])
@app.route("/reports/generate/ba/<hat_filter>/<durak_filter>", methods=['GET', 'POST'])
def ba(hat_filter=None, durak_filter=None):
    hb = HatBasBitDurak()
    df = hb.fetch()
    df = df.head(100)
    ba_rapor = BARapor(df.hatbasbitdurak_df)
    result = ba_rapor.generate(1001)
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
