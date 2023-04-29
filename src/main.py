from crypt import methods
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
        