import random
import time
from flask import request
from src.error import APIError, BadRequestError, ErrorMapper, NotFoundError, UnauthorizedError
from src import db, app, client, socketio
import sys 
import requests



@app.route('/')
def hello_world():

    for coll in db.list_collection_names():
        print(coll)
    return 'hello world'

@app.route('/login', methods=["POST"])
def login():
    
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        existedUser = db.User.find_one(
            {
                "username":username
            }
        )
    
        if not(existedUser):
            raise NotFoundError("user not found")
        
        if existedUser:
            if existedUser['password'] != password:
                raise UnauthorizedError("password is incorrect")

            userId = str(existedUser['_id'])    
            return {
                "message": "login successfully",
                "username": username,
                "id": userId
            }

    except APIError as error:
        return ErrorMapper.mappError(error)
        

@app.route('/signup', methods=["POST"])
def signup():
    
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        existedUser = db.User.find_one(
            {
                "username": username
            })
        
        if existedUser:
            raise BadRequestError("user is existed")

        if not(existedUser):
            user = db.User.insert_one(
            {
                "username":username,
                "password": password
            })

            userId = user.inserted_id

            return {
                "message": "signup successfully",
                "username": username,
                "id": userId
            }
        
    except APIError as error:
        return ErrorMapper.mappError(error)





@app.route("/thermos/", methods=["GET"])
def getThermos():
    try:
        existedThermos = db.Thermo.find({})

        return {
            "message": "update successfully",
            "data": [   {
                            "name": element["name"],
                            "imageUrl": element["imageUrl"]
                        } for element in existedThermos]
        }
        
    except APIError as error:
        return ErrorMapper.mappError(error) 

@app.route("/thermos/<id>", methods=["PATCH"])
def updateThermoDetail(id):
    print('here')
    try:
        data = request.get_json()
        newName = None if 'name' not in data else data['name']
        newImageUrl = None if 'imageUrl' not in data else data['imageUrl']

        if not(newName or newImageUrl):
            raise BadRequestError("All fields are empty")

        print(id)

        existedThermo = db.Thermo.find_one(
            {
                "feed_id": id
            })
        
        if not(existedThermo):
            raise NotFoundError("thermo not found")
        
        if existedThermo:
            if newName and existedThermo['name'] != newName:
                existedThermo['name'] = newName
            if newImageUrl and existedThermo['imageUrl'] != newImageUrl:
                existedThermo['imageUrl'] = newImageUrl

            db.Thermo.find_one_and_update(
            {
                "feed_id":id
            }, 
            {
                "$set":{
                            "name": existedThermo['name'],
                            "imageUrl" : existedThermo['imageUrl']
                        }
            })

            return {
                "message": "update successfully",
            }
        
    except APIError as error:
        return ErrorMapper.mappError(error)
   

@app.route("/lamps/", methods=["GET"])
def getLamps():
    try:
        existeLamps = db.Lamp.find({})

        return {
            "message": "update successfully",
            "data": [   {
                            "lamp_id": element["lamp_id"],
                            "status": element["status"],
                            "name": element["name"],
                            "imageUrl": element["imageUrl"]
                        } for element in existeLamps]
        }
        
    except APIError as error:
        return ErrorMapper.mappError(error) 

@app.route("/lamps/<id>", methods=["PATCH"])
def updateLampDetail(id):
    print('here')
    try:
        data = request.get_json()
        newName = None if 'name' not in data else data['name']
        newImageUrl = None if 'imageUrl' not in data else data['imageUrl']
        newStatus = None if 'status' not in data else data['status'] 
        print(newName,newImageUrl,newStatus)

        if not(newName or newImageUrl or newStatus):
            raise BadRequestError("All fields are empty")

        existedLamp = db.Lamp.find_one(
            {
                "lamp_id": id
            })
        
        if not(existedLamp):
            raise NotFoundError("lamp not found")
        
        if existedLamp:
            if newName and existedLamp['name'] != newName:
                existedLamp['name'] = newName
            if newImageUrl and existedLamp['imageUrl'] != newImageUrl:
                existedLamp['imageUrl'] = newImageUrl
            if newStatus and existedLamp['status'] != newStatus:
                existedLamp['status'] = newStatus


            db.Lamp.find_one_and_update(
            {
                "lamp_id":id
            }, 
            {
                "$set":{
                            "name": existedLamp['name'],
                            "imageUrl" : existedLamp['imageUrl'],
                            "status":existedLamp['status']
                        }
            })

            return {
                "message": "update successfully",
            }
        
    except APIError as error:
        return ErrorMapper.mappError(error)
   

@app.route('/logs', methods=["GET"])
def getLogs():
    try:
        existeLogs = db.Log.find({})

        return {
            "message": "get logs successfully",
            "data": [   {
                
                            "id": str(element["_id"]),
                            "content": element["content"],
                            "time": element["time"],
                        } for element in existeLogs]
        }
        
    except APIError as error:
        return ErrorMapper.mappError(error) 

@app.route('/logs', methods=["POST"])
def createLog():
    
    try:
        data = request.get_json()
        content = data['content']
        time = data['time']

        newLog = db.Log.insert_one(
        {
            "content":content,
            "time": time
        })

        newLogId = str(newLog.inserted_id)

        print(newLogId)
        return {
            "message": "create log successfully",
            "content": content,
            "time": time,
            "id": newLogId
        }
        
    except APIError as error:
        return ErrorMapper.mappError(error)

# @app.route('/fans', methods=["PATCH"])
def updateFan(status: str):
    try:
        # data = request.get_json()
        # newStatus = None if 'status' not in data else data['status']

        # if not(newStatus):
            # raise BadRequestError("All fields are empty")

        existedFan = db.Fan.find_one(
            {
                "fan_id": '1'
            })
        
        if not(existedFan):
            raise NotFoundError("fan not found")
        
        if existedFan:
            existedFan['status'] = status
            

            db.Fan.find_one_and_update(
            {
                "fan_id": '1'
            }, 
            {
                "$set":{
                            "status": existedFan['status'],
                        }
            })

            return {
                "message": "update successfully",
            }
        
    except APIError as error:
        return ErrorMapper.mappError(error)







def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('smart-home.temp')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    socketio.emit('new_temp', {'message': payload})

    if payload > "30" and db.Fan.find({})[0]["status"] == "off":
        print('heat hight')
        requests.post('https://io.adafruit.com/api/v2/lnminhthu1505/feeds/smart-home.fan/data', data = {"value":"1"}, headers = {"X-AIO-Key": "aio_teLx19UtogwB52wolFfreAFt5UVd"})
        
        updateFan("on")

        socketio.emit('turn_fan_on', {'message': payload})

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()
# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
# while True:
#     value = random.randint(0, 100)
#     print('Publishing {0} to DemoFeed.'.format(value))
#     # client.publish('DemoFeed', value)
#     time.sleep(10)



