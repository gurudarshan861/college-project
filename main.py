from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask.json.tag import PassDict
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from tkinter import *

#my db connection
local_server= True
app = Flask(__name__)
app.secret_key='likhith'

#this is for getting unique  user acess
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#this whole login manager stuff is written just to get the name of the current user who has logged in

#this is used to connect flask to database
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/bbms' 
db=SQLAlchemy(app)

#here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True )
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class Request(db.Model):
    r_id=db.Column(db.Integer,primary_key=True)
    Hospital_Name=db.Column(db.String(50))
    Hospital_Address=db.Column(db.String(100))
    Phone_Number=db.Column(db.String(50))
    Email=db.Column(db.String(50))
    Blood_Group=db.Column(db.String(10))
    Number_Of_Packets=db.Column(db.String(50))

class Request_History(db.Model):
    r_id=db.Column(db.Integer,primary_key=True)
    Hospital_Name=db.Column(db.String(50))
    Hospital_Address=db.Column(db.String(100))
    Phone_Number=db.Column(db.String(50))
    Email=db.Column(db.String(50))
    Blood_Group=db.Column(db.String(10))
    Number_Of_Packets=db.Column(db.String(50))
    Status=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Donor(db.Model):
    D_ID=db.Column(db.Integer,primary_key=True)
    DONOR_NAME=db.Column(db.String(50))
    GENDER=db.Column(db.String(100))
    PHONE_NUMBER=db.Column(db.Integer)
    EMAIL=db.Column(db.String(50))
    AGE=db.Column(db.Integer)
    WEIGHT=db.Column(db.Integer)
    ADDRESS=db.Column(db.String(50))
    DISEASE=db.Column(db.String(50))
    BLOOD_GROUP=db.Column(db.String(50))
    DONOR_DATE=db.Column(db.String(50))
    E_ID=db.Column(db.Integer)


class Donation(db.Model):
    donation_id=db.Column(db.Integer,primary_key=True)
    donor_id=db.Column(db.Integer)
    donor_name=db.Column(db.String(50))
    blood_group=db.Column(db.String(1000))
    packets_donated=db.Column(db.Integer)

class Blood_packet(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    blood_group=db.Column(db.String(1000))
    packets_avaliable=db.Column(db.Integer)




@app.route("/") 
def home():
  return render_template('home.html')
@app.route("/request_blood",methods=['POST','GET']) 
def request_blood():
  if request.method=="POST":
        Hospital_Name=request.form.get('Hospital_Name')
        Hospital_Address=request.form.get('Hospital_Address')
        Phone_Number=request.form.get('Phone_Number')
        Email=request.form.get('Email')
        Blood_Group=request.form.get('Blood_Group')
        Number_Of_Packets=request.form.get('Number_Of_Packets')
        Status='Pending'
        query=db.engine.execute(f"INSERT INTO `request` (`Hospital_Name`,`Hospital_Address`,`Phone_Number`,`Email`,`Blood_Group`,`Number_Of_Packets`) VALUES ('{ Hospital_Name}','{ Hospital_Address}','{Phone_Number}','{Email}','{Blood_Group}','{Number_Of_Packets}')")    
        query1=db.engine.execute(f"INSERT INTO `request_history` (`Hospital_Name`,`Hospital_Address`,`Phone_Number`,`Email`,`Blood_Group`,`Number_Of_Packets`,`Status`) VALUES ('{ Hospital_Name}','{ Hospital_Address}','{Phone_Number}','{Email}','{Blood_Group}','{Number_Of_Packets}','{Status}')")
        flash("Request has been placed successfully","danger")
  return render_template('request.html')
@app.route("/signup",methods=['POST','GET']) 
def signup():
  if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password= request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("email already exists","warning")
            return render_template("/signup.html")
        encpassword=generate_password_hash(password)
        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`)VALUES('{username}','{email}','{encpassword}');")
        # newuser=User(username=username,email=email,password=password)
        # db.session.add(newuser)
        # db.session.commit()
        #this is another way of inserting values into the table without using the sql syntax
        flash("Signup Success Please Login","success")
        return render_template('login.html')


  return render_template('signup.html')
@app.route("/login",methods=['POST','GET']) 
def login():
  if request.method=="POST":#here need to import request  to use this similarly session and redirect will let you know when i use it
        email=request.form.get('email')
        password= request.form.get('password')
        # print(email,password) for conformation we will write this
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('acommon'))#return to homepage
        else:
            flash("invalid password","danger")
            return render_template('login.html')
  return render_template('login.html')

@app.route("/acommon")
def acommon():
    return render_template('acommon.html')
@app.route("/bloodrequest",methods=['POST','GET'])
def bloodrequest():
    query=db.engine.execute(f"SELECT * FROM `request`")
    if request.method == 'POST':
            if request.form.get('Button') == 'Accept':
                # pass
                print("Accept")
            elif  request.form.get('Button') == 'Decline':
                # pass # do something else
                print("Decline")
    return render_template('bloodrequest.html',query=query)

@app.route("/donor",methods=['POST','GET'])
def donor():
    query=db.engine.execute(f"SELECT `id` FROM `user`")
    if request.method=="POST":
        Name=request.form.get('Donor_Name')
        Gender=request.form.get('Gender')
        Phone_Number= request.form.get('Phone_Number')
        Email=request.form.get('Email')
        Age=request.form.get('Age')
        Weight=request.form.get('Weight')
        Address=request.form.get('Address')
        Disease=request.form.get('Disease')
        Blood_Group=request.form.get('Blood_Group')
        Employee_Id=request.form.get('E_id')
        new_user=db.engine.execute(f"INSERT INTO `donor` (`DNAME`,`GENDER`,`DPHONENUMBER`,`DEMAIL`,`AGE`,`WEIGHT`,`ADDRESS`,`DISEASE`,`BLOOD_GROUP`,`E_ID`)VALUES('{Name}','{Gender}','{Phone_Number}','{Email}','{Age}','{Weight}','{Address}','{Disease}','{Blood_Group}','{Employee_Id}');")
        # newuser=User(username=username,email=email,password=password)
        # db.session.add(newuser)
        # db.session.commit()
        #this is another way of inserting values into the table without using the sql syntax
        flash("ADDED DONOR SUCCESSFULLY","success")

    return render_template('donor.html',query=query)


@app.route("/donorlogs",methods=['POST','GET'])
def donorlogs():
    query=db.engine.execute(f"SELECT * FROM `donor`")
    return render_template('donorlogs.html',query=query)

@app.route("/donate",methods=['POST','GET'])
def donate():
    query=db.engine.execute(f"SELECT * FROM `donor`")
    query1=db.engine.execute(f"SELECT * FROM `donor`")
    query2=db.engine.execute(f"SELECT * FROM `donor`")
    query3=db.engine.execute(f"SELECT * FROM `donor`")
    if request.method=="POST":
        donor_id=request.form.get('donor_id')
        donor_name=request.form.get('donor_name')
        blood_group=request.form.get('Blood_Group')
        packets_donated=request.form.get('Packets_Donated')
        new_user=db.engine.execute(f"INSERT INTO `donation` (`donor_id`,`donor_name`,`blood_group`,`packets_donated`)VALUES('{donor_id}','{donor_name}','{blood_group}','{packets_donated}');")
        flash("DONATION ACCEPTED","WARNING")
        new_user1=db.engine.execute(f"UPDATE `blood_packet` SET `packets_avaliable`=`packets_avaliable`+'{packets_donated}' WHERE `blood_group`='{blood_group}'")

    return render_template('donate.html',query=query,query1=query1,query2=query2,query3=query3)



@app.route("/dashboard",methods=['POST','GET'])
def dashboard():
    query=db.engine.execute(f"SELECT * FROM `blood_packet`;")


    return render_template('dashboard.html',query=query)

@app.route("/accepted/<string:r_id>/<string:Blood_Group>/<string:Number_Of_Packets>")
def accepted(r_id,Blood_Group,Number_Of_Packets):
    a=r_id
    b='Accepted'
    c=Blood_Group
    d=Number_Of_Packets
    new_user1=db.engine.execute(f"UPDATE `blood_packet` SET `packets_avaliable`=`packets_avaliable`-'{d}' WHERE `blood_group`='{c}'")
    query=db.engine.execute(f"DELETE FROM `request` WHERE r_id='{a}'")
    query1=db.engine.execute(f"UPDATE `request_history` SET `Status`='{b}' WHERE r_id='{a}';")
    query3=db.engine.execute(f"SELECT * FROM `request_history` WHERE `Status`='{b}' ;")


    return render_template('accept.html',query3=query3)


@app.route("/declined/<string:r_id>")
def declined(r_id):
    a=r_id
    b='Declined'
    query=db.engine.execute(f"DELETE FROM `request` WHERE r_id='{a}'")
    query1=db.engine.execute(f"UPDATE `request_history` SET `Status`='Declined' WHERE r_id='{a}';")
    query3=db.engine.execute(f"SELECT * FROM `request_history` WHERE `Status`='{b}' ;")
    return render_template('decline.html',query3=query3)

@app.route("/test")
def test():
    try:
        Test.query.all()
        return 'My database is connected'
    except:
        return 'my db is not connected'

app.run(debug=True)