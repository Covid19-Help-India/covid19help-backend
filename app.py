from os import environ
from flask import Flask, render_template, jsonify, Response, request, redirect, json, render_template_string
import pymongo
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
from datetime import datetime
from dateutil.tz import gettz
from flask_cors import CORS, cross_origin
import bcrypt

# str(environ["MONGO_CONN_URL"])
# str(environ["MONGO_DB"])
# str(environ["MONGO_COL"])
MONGO_USER = "Users"
MONGO_CONN_URL = "mongodb+srv://param_batavia:Esld1IbI4l8xFodc@clustercoviddb.tk0jt.mongodb.net/Covid19Db?retryWrites=true&w=majority"
MONGO_DB = "Covid19Db"
MONGO_COL = "MainColl"
print("App Starts")
client = pymongo.MongoClient(str(MONGO_CONN_URL))
mydb = client[str(MONGO_DB)]
mycol = mydb[str(MONGO_COL)]
mylogin = mydb[str(MONGO_USER)]
print(client)


app = Flask(__name__)
CORS(app)

# app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/add_info', methods=['POST', 'GET'])
def add_info():
    if request.method == 'POST':
        # City, State, Category, Distributor Name, Phone Number, Address, Upvotes, Downvotes  UpdownDetails
        insert_data = {}
        insert_data['City'] = request.form['City']
        insert_data['State'] = request.form['State']
        insert_data['Category'] = request.form['Category']
        insert_data['Distributor'] = request.form['Distributor']
        insert_data['DistPhNo'] = request.form['DistPhNo']
        insert_data['DistAddress'] = request.form['DistAddress']
        insert_data['Upvotes'] = int(0)
        insert_data['Downvotes'] = int(0)
        insert_data['Details'] = request.form['Details']
        insert_data['Pincode'] = request.form['Pincode']
        insert_data['Source'] = request.form['Source']
        try:
            x = mycol.insert_one(insert_data)
            insert_data['status'] = True
        except:
            insert_data['status'] = False
        insert_data['id'] = str(x.inserted_id)
        insert_data.pop('_id')
        print(insert_data)
        response = app.response_class(
            response=dumps(insert_data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/del_info', methods=['POST', 'GET'])
def del_info():
    if request.method == 'POST':
        #data = json.loads(request.get_json())
        # print(data)
        # print(type(data))
        delete_data = {}
        obj_id = request.form['id']
        myquery = {u"_id": ObjectId(u""+str(obj_id))}
        try:
            x = mycol.delete_one(myquery)
            delete_data['status'] = True
        except:
            delete_data['status'] = False
        response = app.response_class(
            response=dumps(delete_data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/edit_info', methods=['POST', 'GET'])
def edit_info():
    if request.method == "POST":
        update_data = {}
        update_data['City'] = request.form['City']
        update_data['State'] = request.form['State']
        update_data['Category'] = request.form['Category']
        update_data['Distributor'] = request.form['Distributor']
        update_data['DistPhNo'] = request.form['DistPhNo']
        update_data['DistAddress'] = request.form['DistAddress']
        update_data['Upvotes'] = request.form['Upvotes']
        update_data['Downvotes'] = request.form['Downvotes']
        update_data['Details'] = request.form['Details']
        update_data['Pincode'] = request.form['Pincode']
        update_data['Source'] = request.form['Source']
        print(update_data)
        obj_id = request.form['id']
        myquery = {u"_id": ObjectId(u""+str(obj_id))}
        newvalues = {"$set": update_data}
        # newvalues = {"$set": {
        #     u""+str(request.form["update_field"]): str(request.form['update_value'])}}
        try:
            x = mycol.update_one(myquery, newvalues)
            update_data['status'] = True
        except:
            update_data['status'] = False
        update_data['id'] = request.form['id']
        response = app.response_class(
            response=dumps(update_data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/get_info', methods=['POST', 'GET'])
def get_info():
    print("Comes Here 0")
    print(request)
    if request.method == 'POST':
        # query_dict = {u'State':str(request.form['State']),u'Category':str(request.form['Category']),u'City':str(request.form['City'])}
        print("Works here 0")
        # query_dict = {u'City': str(request.form['City'])}
        # print("Works here 1", query_dict)
        mydoc = mycol.find()
        print("Works here 2", mydoc)
        json_docs = [doc for doc in mydoc]
        json_data = []
        for doc in json_docs:
            json_data.append({
                "id": str(doc["_id"]),
                "City": str(doc["City"]),
                "State": str(doc["State"]),
                "Category": str(doc["Category"]),
                "Distributor": str(doc["Distributor"]),
                "DistPhNo": str(doc["DistPhNo"]),
                "DistAddress": str(doc["DistAddress"]),
                "Upvotes": str(doc["Upvotes"]),
                "Downvotes": str(doc["Downvotes"]),
                "Details": str(doc["Details"]),
                "Source": str(doc["Source"]),
                "Pincode": str(doc["Pincode"])
            })
        response = app.response_class(
            response=dumps(json_data),
            status=200,
            mimetype='application/json'
        )
        return response
    print("Shouldnt come here")
    failure = {"id": "No Recognized Hit!"}
    response = app.response_class(
        response=dumps(failure),
        status=404,
        mimetype='application/json'
    )
    return response


@app.route('/upvote', methods=['POST', 'GET'])
def upvote():
    if request.method == 'POST':
        obj_id = request.form['id']
        print(obj_id)
        query_dict = mycol.find_one({"_id": ObjectId(u""+str(obj_id))})
        upv = int(query_dict["Upvotes"])
        upv = upv + 1
        query_dict["Upvotes"] = upv
        # dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
        dtobj = datetime.now(tz=gettz('Asia/Kolkata')
                             ).strftime('%H:%M:%S %d-%m-%Y')
        query_dict["Details"] = "Upvoted at " + \
            str(dtobj)
        myquery = {"_id": ObjectId(u""+str(obj_id))}
        newvalues = {"$set": {u"Upvotes": int(
            query_dict["Upvotes"]), u"Details": query_dict["Details"]}}
        upvote_data = {}
        try:
            x = mycol.update_one(myquery, newvalues)
            print(x)
            upvote_data['status'] = True
        except:
            upvote_data['status'] = False
        response = app.response_class(
            response=dumps(upvote_data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/downvote', methods=['POST', 'GET'])
def downvote():
    if request.method == 'POST':
        obj_id = request.form['id']
        print(obj_id)
        query_dict = mycol.find_one({"_id": ObjectId(u""+str(obj_id))})
        upv = int(query_dict["Downvotes"])
        upv = upv + 1
        query_dict["Downvotes"] = upv
        # dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
        dtobj = datetime.now(tz=gettz('Asia/Kolkata')
                             ).strftime('%H:%M:%S %d-%m-%Y')
        query_dict["Details"] = "Downvoted at " + \
            str(dtobj)
        myquery = {"_id": ObjectId(u""+str(obj_id))}
        newvalues = {"$set": {u"Downvotes": int(
            query_dict["Downvotes"]), u"Details": query_dict["Details"]}}
        downvote_data = {}
        try:
            x = mycol.update_one(myquery, newvalues)
            print(x)
            downvote_data['status'] = True
        except:
            downvote_data['status'] = False
        response = app.response_class(
            response=dumps(downvote_data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/login', methods=['POST', 'GET'])
def login():
    print("Code Left Updated!")
    if request.method == 'POST':
        # user = mylogin.
        # if bcrypt.checkpw(password.encode('utf-8'), passwordcheck)
        # og : if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        login_user = mylogin.find_one(
            {u'username': str(request.form['username'])})
        if login_user:
            if request.form['password'] == login_user['password']:
                status = {}
                print("user n pass match")
                status["success"] = True
                status["username"] = str(request.form['username'])
                response = app.response_class(
                    response=dumps(status),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                status = {}
                status["success"] = False
                status["message"] = "Your password is incorrect."
                response = app.response_class(
                    response=dumps(status),
                    status=200,
                    mimetype='application/json'
                )
                return response
        else:
            status = {}
            status["success"] = False
            status["message"] = "Account doesnt exist."
            response = app.response_class(
                response=dumps(status),
                status=200,
                mimetype='application/json'
            )
            return response


        # username = request.body['username'] #same for pass
        # passw = request.body['password']
if __name__ == '__main__':
    app.run(debug="True")
