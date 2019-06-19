# Solardata Service API

This API will get data of a raspberry pi database wich is connected with a sunnyboy solar inverter. The database is created by [SBFspot with SQLite](https://github.com/SBFspot/SBFspot/wiki/Installation-Linux-SQLite).

![GitHub Logo](/img/Solar_service.png)
## 1. Install SBFspot
Follow this [tutorial](https://github.com/SBFspot/SBFspot/wiki/Installation-Linux-SQLite)

## 2. Make your app

### Map structure:
smadata (folder)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;├── API (folder)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── solar_service (folder)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `__init__.py`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;├── `requirements.txt`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;├── `run.py`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;├── SBFspot.db

### Files:
* `run.py:`
```python
from solar_service import app

app.run(host='0.0.0.0', port=80, debug=True)
```
* `__init__.py:`
```python
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
```
* `requirements.txt:`
```txt
Flask==1.0.2
Flask-Cors
sqlite3
```
## 3. Use API
Send a POST request to the ip of the pi with ?query= + the querystring you want to access.
#### example:
* [Pi IpAdress]?query=SELECT * FROM SpotData
