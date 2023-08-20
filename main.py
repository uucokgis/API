from flask import Flask
from reports import *
from yeniden.ba_rapor import BARapor
from yeniden.hatbasbitdurak import HatBasBitDurak
from yeniden.tests import ReportTests

app = Flask(__name__)


@app.route("/reports/generate/ba")
def ba():
    df = ReportTests.mock_hatbasbitdurak() # todo
    ba_rapor = BARapor(df.hatbasbitdurak_df)
    ba_rapor.generate()
    return "<p>Hello, World!</p>"


@app.route("/reports/generate/durak-garaj")
def durak_garaj():
    return "<p>Hello, World!</p>"


@app.route("/reports/generate/durak-gar")
def durak_gar():
    return "<p>Hello, World!</p>"


@app.route("/reports/generate/garaj-garaj")
def garaj_garaj():
    return "<p>Hello, World!</p>"


app.run(debug=True)
