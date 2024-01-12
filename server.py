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

def fetch_facts():
    data = cache.get('facts_data')
    if data is None:
        data = requests.get('https://cat-fact.herokuapp.com/facts').content
        data = json.loads(data)
        cache.set('facts_data', data)
    return data

def fetch_detail(id):
    data = cache.get('facts_detail' + id)
    if data is None:
        data = requests.get('https://cat-fact.herokuapp.com/facts/' + id).content
        data = json.loads(data)
        cache.set('facts_detail' + id, data)
    facts_detail = CatFactDetailModel(data)
    return facts_detail

def fetch_random():
    data = requests.get('https://cat-fact.herokuapp.com/facts/random').content
    data = json.loads(data)
    return fetch_detail(data['_id'])

@app.route("/")
def index():
    return render_template("index.html", active_page="index")

@app.route("/facts")
def facts():
    try:
        facts = fetch_facts()
        fact_list = []
        for fact in facts:
            fact_list.append(CatFactModel(fact))
        return render_template("facts_list.html", active_page="facts", facts=fact_list, error=False)
    except Exception as e:
        return render_template("facts_list.html", active_page="facts", facts=[] , error=True)
    
@app.route("/facts/<id>")
def facts_detail(id):
    try:
        fact = fetch_detail(id)
        return render_template("details_modal.html", active_page="facts", fact=fact, error=False)
    except Exception as e:
        return render_template("details_modal.html", active_page="facts", error=True)

@app.route("/random")
def random():
    fact = fetch_random()
    return render_template("random.html", active_page="random", fact=fact)

if __name__ == "__main__":
    app.run(debug=True)