from tkinter import ON
from flask import Flask, render_template, request
import numpy as np
from functions import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/charts', methods=["POST"])
def charts():
    fi = request.form.get('fi')
    lam = request.form.get('lam')
    h = request.form.get('h')
    date = request.form.get('data')
    mask = request.form.get('mask')

    if not fi or not lam or not h or not date or not mask:
        error_statement = "Wszystkie rubryki muszą być wypełnione!"
        return render_template('index.html', error_statement=error_statement, fi=fi, lam=lam, h=h, date=date, mask=mask)

    if request.form.get('checkbox'):
        almanac = new_almanac()
    else:
        if not request.form.get('almanac'):
            error_statement = "Nie wybrano almanachu!"
            return render_template('index.html', error_statement=error_statement, fi=fi, lam=lam, h=h, date=date, mask=mask)

        almanac = read_yuma(request.form.get('almanac'))

    day = int(date[8:10])
    month = int(date[5:7])
    year = int(date[0:4])
    dateOfMeasure = [year, month, day, 0, 0, 0]
    hours = list(range(0, 25))
    minutes = list(range(0, 1500, 10))
    az, el, dops, sat_nr, el_sky, az_sky, sat_name = all_day_sat(
        float(fi), float(lam), float(h), dateOfMeasure, almanac, int(mask))
    return render_template('charts.html', hours=hours, dops=dops, elev=el, minutes=minutes, sat_nr=sat_nr, az_sky=az_sky, el_sky=el_sky, sat_name=sat_name)


if __name__ == '__main__':
    app.run()
