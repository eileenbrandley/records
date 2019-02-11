from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

import sqlite as sq
from homedata import HomeData

app = Flask(__name__)



def get_is_female(gender):
    if gender == 'All':
        return [0, 1]
    else:
        return 1 if gender == "F" else 0


def get_race_params(params):
    if params is None:
        return None

    race_params = {}

    if 'gender' in params.keys():
        gender = request.args.get('gender', 'All')
        race_params['gender'] = get_is_female(gender)

    if 'option'in params.keys():
        d = params['option']
        race_params['option'] = request.args.get('option', d[list(d)[0]])

    return race_params


def convert_query_to_dict(query_string, db):
    return {d[0]: d[1] for d in sq.fetch_data(query_string, db)[1:]}


def get_options_from_query(params, key):
    if key in params.keys() and not isinstance(params[key], dict):
        params[key] = convert_query_to_dict(params[key], 'records')
    return params


@app.route("/")
def index():
    home_data = HomeData()
    return render_template('home.html', queries=home_data.queries)


@app.route("/view/<query_id>", methods=["GET"])
def view_query(query_id):
    query = f"SELECT file_name, title, params FROM queries WHERE id = {query_id}"
    query_data = sq.fetch_data(query, 'queries')[1]

    file_name = query_data[0]
    title = query_data[1]
    form_params = json.loads(query_data[2])


    form_params = get_options_from_query(form_params, 'option')

    query_params = get_race_params(form_params)

    file_path = os.path.dirname(os.path.realpath(__file__))

    data = sq.fetch_data_from_file(
        f'{file_path}/../sql/{file_name}.sql',
        'records',
        query_params)

    return render_template(
        'query.html',
        data=json.dumps(data),
        title=title,
        form_params=form_params,
        query_params=query_params)


@app.route("/view/<query_id>", methods=["POST"])
def post_query(query_id):
    option = request.form.get('option')
    gender = request.form.get('gender')
    return redirect(f"/view/{query_id}?option={option}&gender={gender}", code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')