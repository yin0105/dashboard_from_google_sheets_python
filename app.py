#!/usr/bin/env python
from flask import Flask, render_template, request, flash, redirect, url_for, g, session
from flask_bootstrap import Bootstrap
from models import UserForm, LoginForm
# from flask_datepicker import datepicker
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import json
# # from proxy import MyThread, proxy_status, proxies_list
from sqlalchemy_serializer import SerializerMixin
# import requests
# from bs4 import BeautifulSoup
import os
# import pprint
from werkzeug.utils import secure_filename

class Config(object):
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dashboard_google_sheet'
app.config['SECRET_KEY'] = "3489wfksf93r2k3lf9sdjkfe9t2j3krl"

Bootstrap(app)
# datepicker(app)
db = SQLAlchemy(app)
dir_path = os.path.dirname(os.path.realpath(__file__))

# class country_1(db.Model):
#    short = db.Column(db.String(10), primary_key = True)
#    country = db.Column(db.String(50))

# class country_2(db.Model):
#    short = db.Column(db.String(10), primary_key = True)
#    country = db.Column(db.String(50))

# class country_3(db.Model):
#    short = db.Column(db.String(10), primary_key = True)
#    country = db.Column(db.String(50))

class User(db.Model, SerializerMixin):  
    __tablename__ = 'user'

    serialize_only = ('name', 'user_id', 'password', 'email', 'phone', 'dates', 'locations')
    
    name =  db.Column(db.String(30), nullable = False) 
    user_id =  db.Column(db.String(30), nullable = False) 
    password =  db.Column(db.String(30), nullable = False) 
    email = db.Column(db.String(30), nullable = False) 
    phone = db.Column(db.String(20), nullable = False) 
    dates = db.Column(db.String(500), nullable = False)
    locations = db.Column(db.String(), nullable = False) 
    status = db.Column(db.Integer, default = 0) 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    def __init__(self, name, user_id, password, email, phone, dates, locations):
        self.name = name
        self.user_id = user_id
        self.password = password        
        self.email = email
        self.phone = phone
        self.dates = dates
        self.locations = locations

class Company(db.Model, SerializerMixin):  
    __tablename__ = 'company'

    serialize_only = ('comp_name', 'cnpj', 'email', 'logo', 'standard_rate', 'improved_rate')
    
    comp_name =  db.Column(db.String(50), nullable = False) 
    cnpj =  db.Column(db.String(30), primary_key=True, nullable = False) 
    email = db.Column(db.String(50), nullable = False) 
    logo = db.Column(db.String(50), nullable = False) 
    standard_rate = db.Column(db.Float, nullable = False) 
    improved_rate = db.Column(db.Float, nullable = False)


    def __init__(self, comp_name, cnpj, email, logo, standard_rate, improved_rate):
        self.comp_name = comp_name
        self.cnpj = cnpj
        self.email = email
        self.logo = logo        
        self.standard_rate = standard_rate
        self.improved_rate = improved_rate


@app.route('/', methods=['GET', 'POST'])
def admin():
    return render_template('main.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    return render_template('user.html')

@app.route('/company', methods=['GET', 'POST'])
def company():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    if request.method == 'POST':
        print("Len = " + str(len(request.form)))
        for ff in request.form:
            print(ff)
        f = request.files['logo']
        if f.filename != '':
            f.save(dir_path + "\\static\\app-assets\\images\\company_logo\\" + secure_filename(f.filename))
        comp = Company(request.form['comp_name'], request.form['cnpj'], request.form['email'], f.filename, request.form['standard_rate'], request.form['improved_rate'])
            
        db.session.add(comp)
        db.session.commit()
    companies = Company.query.order_by(Company.comp_name)
    return render_template('company.html', comps=companies)


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#         f = request.files['file']
#         if f.filename != '':
#             f.save(dir_path + "\\static\\app-assets\\images\\company_logo\\" + secure_filename(f.filename))
    
#       return 'file uploaded successfully'


# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     # print(request.form['name'] + "::::::" + request.form['password'])
#     if request.method == 'POST':
#         if os.environ.get('ADMIN_NAME') == request.form['name'] and os.environ.get('ADMIN_PASSWORD') == request.form['password']:
#             session['username'] = request.form['name']
#             return redirect(url_for('admin'))
   
#     return render_template('login.html', form=LoginForm())

# @app.route('/logout', methods = ['POST', 'GET'])
# def logout():
#     session.pop("username", None)
#     return redirect(url_for("login"))

# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     form = UserForm(request.form)
    
#     if 'type_' in request.form:# == "save":

#         if not form.validate_on_submit():
#             flash('Please enter all the fields', 'error')
#         else:
#             str = ''
#             for i in range(len(request.form.getlist('td_search[]'))):
#                 if request.form.getlist('td_search[]')[i]:
#                     if str != '' :
#                         str += ','
#                     str += '{"s": "' + request.form.getlist('td_search[]')[i] +'", '
#                     str += '"m": "' + request.form.getlist('td_miles[]')[i] +'", '
#                     str += '"t": "' + request.form.getlist('td_time[]')[i] +'"}'
#             str = '{"locationList":[' + str +']}'

#             user_ = User(request.form['name'], request.form['user_id'], request.form['password'], request.form['email'], request.form['phone'], request.form['dates'], str)
            
#             db.session.add(user_)
#             db.session.commit()
#             flash('Record was successfully added')
#             return redirect(url_for('admin'))   
    
#     form.locations = [{"search": "", "miles": "", "time": ""}]
#     return render_template('user.html', form=form, )


# @app.route('/edit_user', methods=['POST'])
# def edit_user():  
#     form = UserForm(request.form)
    
#     # if request.method == 'POST':
#     if request.form['type_'] == "save":
#         if not form.validate_on_submit():
#             flash('Please enter all the fields', 'error')
#         else:
#             str = ''
#             for i in range(len(request.form.getlist('td_search[]'))):
#                 if request.form.getlist('td_search[]')[i]:
#                     if str != '' :
#                         str += ','
#                     str += '{"s": "' + request.form.getlist('td_search[]')[i] +'", '
#                     str += '"m": "' + request.form.getlist('td_miles[]')[i] +'", '
#                     str += '"t": "' + request.form.getlist('td_time[]')[i] +'"}'
#             str = '{"locationList":[' + str +']}'
           
            
#             db.session.query(User).filter_by(id = request.form['id']).update({User.name: request.form['name'], User.user_id: request.form['user_id'], User.password: request.form['password'], User.email: request.form['email'], User.phone: request.form['phone'], User.dates: request.form['dates'], User.locations: str}, synchronize_session = False)
#             db.session.commit()
#             flash('Record was successfully updated')
#             return redirect(url_for('admin'))   
#     else:
#         user_ = User.query.filter_by(id=request.form['user_id']).first()
#     user_.locations = json.loads(user_.locations)
#     return render_template('user.html', form=form, user=user_)


# @app.route('/del_user/<int:user_id>', methods=['GET', 'POST'])
# def del_user(user_id):
#     db.session.query(User).filter_by(id=user_id).delete()
#     db.session.commit()

#     return ""


# @app.route('/view_log', methods=['POST'])
# def view_log():  
#     log_list = []
#     try:
#         log_file = open('logs/' + request.form['user_id'] + '.log', 'r') 
#         while True: 
#             line = log_file.readline()                
#             if not line: 
#                 break
#             if line.find("/") < 0:
#                 log_list.append(line.strip())                       
#     except:
#         pass
#     return render_template('log.html', log_list = log_list)


# @app.route('/calendar', methods=['GET', 'POST'])
# def calendar():
#     return render_template('calendar.html')


# @app.route('/ajax_get_user_status', methods=['GET', 'POST'])
# def ajax_get_user_status():
#     users = User.query.order_by(User.name)
#     result = ""
#     for user_ in users:
#         if str(user_.id) in proxy_status:
#             result += str(proxy_status[str(user_.id)]) + ","
#         else:
#             result += "0,"
#     result = result[:-1]

#     return result


# @app.route('/start_proxy/<userId>', methods=['GET', 'POST'])
# def start_proxy(userId):
#     try:
#         if proxy_status[userId] >= 1:
#             return ""
#     except:
#         pass

#     proxy_status[userId] = 1
#     print("proxy_status[" + userId + "] = " + str(proxy_status[userId]))
#     db.session.query(User).filter_by(id = userId).update({User.status: 1}, synchronize_session = False)
#     db.session.commit()

#     user_ = User.query.filter_by(id=userId).first()
#     user_.locations = json.loads(user_.locations)

#     t = MyThread(userId, user_.to_dict())
#     t.start()

#     return ""
        

# @app.route('/stop_proxy/<userId>', methods=['GET', 'POST'])
# def stop_proxy(userId):
#     proxy_status[userId] = 0
#     db.session.query(User).filter_by(id = userId).update({User.status: 0}, synchronize_session = False)
#     db.session.commit()
#     return ""



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
