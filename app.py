#env

from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import datetime



app = Flask(__name__)
CORS(app)
db=SQLAlchemy(app)
ma=Marshmallow(app)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='this is the secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

class User(db.Model):
    
    rollno = db.Column(db.String(50),primary_key=True)
    name = db.Column(db.String(50))
    mobile=db.Column(db.String(10))
    branch=db.Column(db.String(10))
    email=db.Column(db.String(10))
    sex=db.Column(db.String(50))
    dob=db.Column(db.DateTime)
    

class User_schema(ma.Schema):
    class Meta:
        fields =('id','rollno','mobile','branch','email','sex','dob','name')


userschema = User_schema()
usersschema = User_schema(many=True)

@app.route('/reg',methods=['POST'])
def reg():
  

        rollno=request.json['rollno']
        mobile=request.json['mobile']
        branch=request.json['branch']
        email=request.json['email']
        sex=request.json['sex']
        dob=request.json['dob']
        name=request.json['name']

        y,m,d=dob.split('-')
        dob=datetime.datetime(int(y),int(m),int(d))

        if(User.query.get(rollno)):
            return make_response("You are already Registered",400)

        if(rollno[-2:].isalpha() and rollno[0].isalpha() and rollno[1:7].isdigit() and mobile.isdigit() ):
            new=User(rollno=rollno,mobile=mobile,branch=branch,email=email,sex=sex,dob=dob,name=name)
            db.session.add(new)
            db.session.commit()

            return userschema.jsonify(new)

        else:
            return make_response("Bad Request",400)
        
   

@app.route("/getall",methods=['GET'])
def getall():
    
        users=User.query.all() 
        results=usersschema.dump(users)
        
        return jsonify(results)

    















if __name__ == '__main__':
    app.run(debug=True)
