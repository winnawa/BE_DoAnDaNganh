from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)

# app.config["SECRET_KEY"] = 
app.config["MONGO_URI"] = "mongodb+srv://winnawa:namkhoapro2804@cluster0.8p7d3.mongodb.net/IoT_control?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)
db = mongodb_client.db

