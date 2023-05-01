from crypt import methods
import re
from urllib import request, response
from flask import request
from src.error import APIError, BadRequestError, ErrorMapper, NotFoundError, UnauthorizedError
from src import db, app

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
        newName = data['name']
        newImageUrl = data['imageUrl']

        if not(newName and newImageUrl):
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
   