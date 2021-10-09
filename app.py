from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars  # pointer to db
    mars_data = scraping.scrape_all()  # scraped data
    mars.update({}, mars_data, upsert=True)  # {} is the query parameter. upsert creates new doc if one doesn't already exist
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run()