import sqlite3

from flask import Flask, redirect, url_for, request
from flask.json import jsonify
import sys

sys.path.append("/home/pi/.local/lib/python3.5/site-packages")
from flask_cors import CORS, cross_origin
print("SYSTEMPATH = ",sys.path)

app = Flask(__name__)
CORS(app, supports_credentials=True)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db(queryString):
    conn = sqlite3.connect('../SBFspot.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(queryString)
    data = c.fetchall()
    conn.close()
    return data

@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def hello_world():
    if request.method == 'POST':
        data = request.args.get('query')
        #print("datais ", data)
        if data != None:
            try:
                queryResult = get_db(data)
                print("queryResult = ", len(queryResult))
                return jsonify(queryResult)
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])
                return e.args[0]
    return "send a request"