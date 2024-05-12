from flask import Flask,render_template,request,jsonify,session
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
from utils import client

load_dotenv()

app = Flask(__name__,template_folder='src')
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl',methods=['POST'])
def crawl():
    if not request.is_json :
        print("here")
    data = request.get_json()
    seed_url = data.get('seed_url')
    keywords = data.get('keywords', [])
    print("heyyyy", seed_url, keywords)
    
    # Ensure that the `main` function returns a dictionary or list that can be serialized
    results = client.crawl_request(seed_url, keywords)
    session['results'] = results
    # Convert results to JSON format and return with the appropriate status
    return jsonify({
        'status': 'success',
        'data': results
    })


@app.route('/result')
def result_page():
    results = session.get('results', [])
    print("here",results)
    # Pass data to the results.html template
    return render_template('result.html',results=results)




if __name__ == '__main__':
    app.run(debug=True)

