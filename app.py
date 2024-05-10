from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl',methods=['POST'])
def crawl():
    seed_url=request.form.get('url')
    keywords = request.form.get('keywords', [])
    message = json.dumps({'seed_url': seed_url, 'keywords': keywords}).encode('utf-8')







if __name__ == '__main__':
    app.run(debug=True)

