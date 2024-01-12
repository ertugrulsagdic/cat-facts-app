from flask import (
    Flask, render_template, json
)
from flask_caching import Cache
import requests
import json
from models.cat_fact_model import CatFactModel
from models.cat_fact_detail_model import CatFactDetailModel

app = Flask(__name__, template_folder='views')
app.config["SECRET_KEY"] = "any random string"
app.config["CACHE_TYPE"] = "SimpleCache"
cache = Cache(app)

def fetch_data(url, cache_key):
    try:
        data = cache.get(cache_key)
        if data is None:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data)
            else:
                return {'error': 'Failed to fetch data from API', 'status_code': response.status_code}, response.status_code
        return data, 200
    except requests.RequestException as e:
        return {'error': 'Network error occurred', 'status_code': 503}, 503
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON received', 'status_code': 500}, 500

def fetch_facts():
    return fetch_data('https://cat-fact.herokuapp.com/facts', 'facts_data')    
   

def fetch_detail(id):
    return fetch_data('https://cat-fact.herokuapp.com/facts/' + id, 'facts_detail' + id)

def fetch_random():
    data = requests.get('https://cat-fact.herokuapp.com/facts/random').content
    data = json.loads(data)
    return fetch_detail(data['_id'])

@app.route("/")
def index():
    return render_template("index.html", active_page="index")

@app.route("/api/fact-table")
def fact_table():
    data, code = fetch_facts()
    response = json.dumps(data)
    return response, code

@app.route("/api/fact-table/<id>")
def fact_table_detail(id):
    data, code = fetch_detail(id)
    response = json.dumps(data)
    return response, code

@app.route("/facts")
def facts():
    facts, code = fetch_facts()
    if code == 200:
        fact_list = []
        for fact in facts:
            fact_list.append(CatFactModel(fact))
        return render_template("facts_list.html", active_page="facts", facts=fact_list, error=False)
    else:
        return render_template("facts_list.html", active_page="facts", facts=[], error=True)
    
@app.route("/facts/<id>")
def facts_detail(id):
    fact, code = fetch_detail(id)
    if code == 200:
        facts_detail = CatFactDetailModel(fact)
        return render_template("details_modal.html", active_page="facts", fact=facts_detail, error=False)
    else:
        return render_template("details_modal.html", active_page="facts", error=True)

@app.route("/random")
def random():
    fact, code = fetch_random()
    if code == 200:
        facts_detail = CatFactDetailModel(fact)
        return render_template("random.html", active_page="random", fact=facts_detail, error=False)
    else:
        return render_template("random.html", active_page="random", error=True)

if __name__ == "__main__":
    app.run(debug=True)