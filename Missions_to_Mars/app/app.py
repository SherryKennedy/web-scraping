from flask import Flask, render_template, redirect, jsonify
#from flask_pymongo 
import pymongo
from pymongo import MongoClient
#from sqlalchemy_utils.functions import database_exists
#if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    # do stuff
import scrape_mars
#import sys

app = Flask(__name__)

# def is_mongo_db_exist(db_name):
     
#      # get all database name list.    
#      db_list = mongodb_client.list_database_names()    
     
#      if db_name in db_list:
         
#          print('Mongo database ', db_name, ' exist.')
         
#          return True
         
#      else:
          
#          print('Mongo database ', db_name, ' do not exist.')

         
#          return False

# Use flask_pymongo to set up mongo connection

# import pymongo
# from pymongo import MongoClient

conn = "mongodb://localhost:27017"
mongodb_client = MongoClient(conn)
#db = client.mars_db

#app.config["MONGO_URI"] = "mongodb://localhost:27017/"
#mongodb_client = PyMongo(app)
db = mongodb_client['mars_db']
#db = mongodb_client.db
print(mongodb_client.list_database_names())

# needs data then will create locally on db

# databaseNames = mongodb_client.getDatabaseNames()
# print(databaseNames)
#if database_exists(app.config["MONGO_URI"]):
    # do stuff
    #print('using db')
#mongodb_client = PyMongo(app)
#db = mongodb_client
#create instance
#db = mongodb_client.db
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
#mongodb_client = MongoClient('localhost', 27017)

#db_name = "mars_db"

#mongodb_client = PyMongo(app)
#db = mongodb_client.db
#b_db_exists = is_mongo_db_exist(db_name)
# print(b_db_exists)
# b_db_exists 
# if b_db_exists:
#     db = mongodb_client.mars_db
# else:
#     # create the database
#     print('creating db')
#     #db = client[db_name]
#     db = mongodb_client[db_name]
#     #mongodb_client['mars_db']
#     #collection_name = 'mars_data' 
#     #db_cm = db[collection_name]
#     print(mongodb_client.list_database_names())   
    


#b_db_exists = is_mongo_db_exist(db_name)
#print(b_db_exists)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def home():
    # find the information
    mars_data = db.mars.find_one()
    #print(mars)
    print(f'Hello: {mars_data}')
    return render_template("index.html",data1=mars_data)
    #return render_template("index.html",data=mars_data)


@app.route("/scrape")
def scraper():
    #listings = mongo.db.listings
    #listings = mongo.db.listings.find_one()
    #return render_template("index.html", listings=listings)
    #need this? - is it creating a new db.mars  instance then getting data for it?
    mars_data_scrape = db.mars
    mars_data_scrape = scrape_mars.scrape()
    print(mars_data_scrape)
    # ok to replace data there, upsert
    db.mars.update({}, mars_data_scrape, upsert=True)
    #listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)



