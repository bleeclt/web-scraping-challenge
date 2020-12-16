from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# route for index.html template using mongo data
@app.route("/")
def index():

    # find record of data from mongo db
    mars_data = mongo.db.mars_data.find_one()
    
    # return template and data
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)