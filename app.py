from os import environ
from flask import Flask, render_template,jsonify, Response, request, redirect, json, render_template_string
import pymongo
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
from datetime import datetime
from dateutil.tz import gettz
from flask_cors import CORS, cross_origin
import bcrypt

#str(environ["MONGO_CONN_URL"])
#str(environ["MONGO_DB"])
#str(environ["MONGO_COL"])
MONGO_USER = "Users"
print("App Starts")
client = pymongo.MongoClient(str(environ["MONGO_CONN_URL"]))
mydb = client[str(environ["MONGO_DB"])]
mycol = mydb[str(environ["MONGO_COL"])]
mylogin = mydb[str(MONGO_USER)]
print(client)



app = Flask(__name__)
CORS(app)

#app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/add_info', methods=['POST', 'GET'])
def add_info():
    if request.method == 'POST':
        #City, State, Category, Distributor Name, Phone Number, Address, Upvotes, Downvotes  UpdownDetails
        insert_data  = {}
        insert_data['City'] = request.form['']
        insert_data['State'] = request.form['']
        insert_data['Category'] = request.form['']
        insert_data['Distributor'] = request.form['']
        insert_data['DistPhNo'] = request.form['']
        insert_data['DistAddress'] = request.form['']
        insert_data['Upvotes'] = int(0)
        insert_data['Downvotes'] = int(0)
        insert_data['Details'] = u''
        insert_data['Source'] = request.form['']
        x  = mycol.insert_one(insert_data)
        return insert_data

@app.route('/del_info', methods=['POST', 'GET'])
def del_info():
    if request.method == 'POST':
        obj_id = request.form['entry_id']
        myquery = {u"_id":ObjectId(u""+str(obj_id))}
        x = mycol.delete_one(myquery)
        success = {}
        success["info"] = x
        response = app.response_class(
                    response=dumps(success),
                    status=200,
                    mimetype='application/json'
                )
        return response

@app.route('/edit_info', methods=['POST', 'GET'])
def edit_info():
    if request.method == "POST":
        obj_id = request.form['entry_id']
        myquery = {u"_id":ObjectId(u""+str(obj_id))}
        newvalues = { "$set": { u""+str(request.form["update_field"]): str(request.form['update_value']) } }
        x  = mycol.update_one(myquery, newvalues)
        success = {}
        success["info"] = x
        response = app.response_class(
                    response=dumps(success),
                    status=200,
                    mimetype='application/json'
                )
        return response





@app.route('/get_info', methods=['POST', 'GET'])
def get_info():
    print("Comes Here 0")
    if request.method == 'POST':
        #query_dict = {u'State':str(request.form['State']),u'Category':str(request.form['Category']),u'City':str(request.form['City'])}
        query_dict = {u'City':str(request.form['City'])}
        print("Works here 1")
        mydoc = mycol.find(query_dict)
        print("Works here 2")
        json_docs = [dumps(doc) for doc in mydoc]
        print("Works here 3")
        response = app.response_class(
                    response=dumps(json_docs),
                    status=200,
                    mimetype='application/json'
                )
        return response
    print("Shouldnt come here")
    failure = {"id":"No Recognized Hit!"}
    response = app.response_class(
                response=dumps(failure),
                status=404,
                mimetype='application/json'
            )
    return response


@app.route('/upvote', methods=['POST', 'GET'])
def upvote():
    if request.method == 'POST':
      obj_id = request.form['entry_id']
      query_dict  = mycol.find_one({"_id" : ObjectId(u""+str(obj_id))})
      query_dict["Upvotes"] += 1
      #dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
      dtobj = datetime.now(tz=gettz('Asia/Kolkata')).strftime('%H:%M:%S %d-%m-%Y')
      query_dict["Details"] = "Upvoted at " + str(dtobj) +   " <br/>" + query_dict["Details"]
      myquery = { "_id": ObjectId(u""+str(obj_id)) }
      newvalues = { "$set": { u"Upvotes": int(query_dict["Upvotes"]), u"Details" : query_dict["Details"] } }
      x  = mycol.update_one(myquery, newvalues)
      success = {}
      success["info"] = "Hopefully success!"
      response = app.response_class(
                  response=dumps(success),
                  status=200,
                  mimetype='application/json'
              )
      return response



@app.route('/downvote', methods=['POST', 'GET'])
def downvote():
    if request.method == 'POST':
      obj_id = request.form['entry_id']
      query_dict  = mycol.find_one({"_id" : ObjectId(u""+str(obj_id))})
      query_dict["Downvotes"] += 1
      #dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
      dtobj = datetime.now(tz=gettz('Asia/Kolkata')).strftime('%H:%M:%S %d-%m-%Y')
      query_dict["Details"] = "Downvoted at " + str(dtobj) +  " for " + request.form['reason'] + " <br/>" + query_dict["Details"]
      myquery = { "_id": ObjectId(u""+str(obj_id)) }
      newvalues = { "$set": { u"Downvotes": int(query_dict["Downvotes"]), u"Details" : query_dict["Details"] } }
      x = mycol.update_one(myquery, newvalues)
      success = {}
      success["info"] = "Hopefully success!"
      response = app.response_class(
                  response=dumps(success),
                  status=200,
                  mimetype='application/json'
              )
      return response

@app.route('/login',methods=['POST','GET'])
def login():
    print("Code Left Updated!")
    if request.method == 'POST':
        #user = mylogin.
        login_user = mylogin.find_one({u'username':str(request.form['username'])})
        if login_user:
             if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                 status = {}
				 print("user n pass match")
                 status["success"] = True
                 status["username"] = login_user
                 response = app.response_class(
                               response=dumps(status),
                               status=200,
                               mimetype='application/json'
                           )
                 return response
             else :
                status = {}
                status["success"] = False
                status["message"] = "Your password is incorrect."
                response = app.response_class(
                              response=dumps(status),
                              status=200,
                              mimetype='application/json'
                          )
                return response
        else :
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
