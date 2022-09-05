import os
from flask import Blueprint, render_template, request, json, url_for

import pickle
import numpy as np

models_path = os.path.join(os.path.dirname(__file__), 'ml_models')
totalCases = pickle.load(open(models_path + '/total_cases.pickle', 'rb'))
totalDeaths = pickle.load(open(models_path + '/total_deaths.pickle', 'rb'))


views = Blueprint('views', __name__, static_folder="static")

data = json.load(open(os.path.join(views.static_folder, 'data.json')))
columns = data['columns']
locations = columns[3:]


def getPrediction(location, year, month, day):
    loc_index = columns.index(location)
    
    x = np.zeros(len(columns))
    x[0] = year
    x[1] = month
    x[2] = day

    if loc_index >= 0:
        x[loc_index] = 1
    print(x)

    return {
        'total_cases': int(totalCases.predict([x])[0])*1000,
        'total_deaths': int(totalDeaths.predict([x])[0])*1000,
    }


@views.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        location = request.form['location']
        date = request.form['date']
        day, month, year = date.split("-")
        message = getPrediction(location, year, month, day)
        message['location'] = location
        message['date'] = date
        return render_template('index.html', locations=locations, message=message)
    return render_template('index.html', locations=locations)