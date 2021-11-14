from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongodb_client = PyMongo(app)


@app.route("/")
def home():
    # find the information
    mars_data = mongodb_client.db.mars.find_one()
    print(f'Hello: {mars_data}')
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data_scrape = scrape_mars.scrape()
    print(mars_data_scrape)
    # ok to replace data there, upsert
    mongodb_client.db.mars.update({}, mars_data_scrape, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)



