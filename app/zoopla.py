from flask import Flask, request, render_template
import sys
from datetime import datetime
import base64
import requests
import os
import json


app = Flask(__name__)

now = datetime.now()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/range", methods=['GET', 'POST'])
def range():
    outcode = request.form['outcode']
    rangee = request.form['range']
    query_string = 'https://api.postcodes.io/outcodes/'+str(outcode)+'/nearest?radius='+str(rangee)
    r = requests.get(query_string)
    status = r.json()
    dicts = status['result']

    ''' to process regex '''
    postcodeArray = []
    outcodeArray = []

    for item in dicts:
        if len(item['outcode']) == 3:
            outcodeArray.append(item['outcode'])
            item['outcode'] = '(' + item['outcode'] + '$)'
            postcodeArray.append(item['outcode'])
        else:
            outcodeArray.append(item['outcode'])
            item['outcode'] = '(' + item['outcode'] + ')'
            postcodeArray.append(item['outcode'])

    '''take the generated regex strings and make a new string'''
    sendString = '|'.join(postcodeArray)

    return render_template("range.html", postcode=outcode, rangee=rangee, response=str(sendString), listarray = str(outcodeArray))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)