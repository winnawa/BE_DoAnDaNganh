from flask import Flask
from flask_pymongo import PyMongo
# from flask_mqtt import Mqtt
from flask_cors import CORS, cross_origin
from Adafruit_IO import MQTTClient

app = Flask(__name__)
cors = CORS(app)

# Config Mongodb
app.config["MONGO_URI"] = "mongodb+srv://winnawa:namkhoapro2804@cluster0.8p7d3.mongodb.net/IoT_control?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)
db = mongodb_client.db

# Config MQTT
app.config['MQTT_CLIENT_ID'] = 'aasasdd'
username = 'lnminhthu1505'
key = 'lnminhthu1505/feeds/smart-home.rgb'
# f"mqtts://{username}:{key}@io.adafruit.com" 
app.config['MQTT_BROKER_URL'] =  "io.adafruit.com"# use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883 # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'lnminhthu1505' # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = key # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5 # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False # set TLS to disabled for testing purposes

# mqtt = Mqtt(app)






# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_teLx19UtogwB52wolFfreAFt5UVd'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'lnminhthu1505'
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)