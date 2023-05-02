from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from Adafruit_IO import MQTTClient
from flask_socketio import SocketIO


app = Flask(__name__)
cors = CORS(app)

# Config Mongodb
app.config["MONGO_URI"] = "mongodb+srv://winnawa:namkhoapro2804@cluster0.8p7d3.mongodb.net/IoT_control?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)
db = mongodb_client.db



# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_teLx19UtogwB52wolFfreAFt5UVd'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'lnminhthu1505'
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



# Socket IO
socketio = SocketIO(app, cors_allowed_origins="*")