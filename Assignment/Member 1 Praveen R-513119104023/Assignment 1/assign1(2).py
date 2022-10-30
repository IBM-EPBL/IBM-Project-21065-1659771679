from flask import Flask,render_template,request
from datetime import *
import requests
from dateutil.relativedelta import *
import numpy as np
import random
import wikipedia

app = Flask(__name__)
@app.route('/')
def student():
    b = np.array([[1,2],[3,4]])
    val = b.size
    r = requests.get('https://api.spotify.com/')
    a = r.status_code
    date = datetime.now()
    words = ['tree','sun','ball','moon','earth','grass','world']
    word = random.choice(words)
    result = wikipedia.page("ID")
    res = result.summary
    return f'Date is {date}<br>Status Code : {a}<br>Array is {b}<br>Array Size : {val}<br>Random word : {word}<br>IBM summary<br>{res}'

if __name__ == '__main__':
    app.run(debug=True)