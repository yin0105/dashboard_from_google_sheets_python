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
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey


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


class User(db.Model, SerializerMixin):  
    __tablename__ = 'user'

    serialize_only = ('name', 'lastname', 'email', 'password', 'photo', 'company', 'approve')
    
    name =  db.Column(db.String(30), nullable = False) 
    lastname =  db.Column(db.String(30), nullable = False)     
    email = db.Column(db.String(50), nullable = False) 
    password =  db.Column(db.String(30), nullable = False) 
    photo = db.Column(db.String(50), nullable = False) 
    companies = db.Column(db.Text, nullable = False) 
    approve = db.Column(db.Boolean, nullable = False) 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, name, lastname, email, password, photo, companies, approve):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password                
        self.photo = photo
        self.companies = companies
        self.approve = approve


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


class Tbl(db.Model, SerializerMixin):  
    __tablename__ = 'tbl'

    serialize_only = ('tbl_name', 'description')
    
    tbl_name =  db.Column(db.String(50), nullable = False) 
    description = db.Column(db.Text, nullable = False) 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, tbl_name, description):
        self.tbl_name = tbl_name
        self.description = description


class Field(db.Model, SerializerMixin):  
    __tablename__ = 'field'

    serialize_only = ('tbl_id', 'from_', 'to', 'rule', 'field_type')
    
    tbl_id =  db.Column(db.Integer, nullable = False) 
    from_ =  db.Column(db.String(50), nullable = False)     
    to = db.Column(db.String(50), nullable = False) 
    rule =  db.Column(db.Text, nullable = False) 
    field_type = db.Column(db.Integer, db.ForeignKey('field_type.id'))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_type = db.relationship('Field_Type')

    def __init__(self, tbl_id, from_, to, rule, field_type):
        self.tbl_id = tbl_id
        self.from_ = from_
        self.to = to
        self.rule = rule                
        self.field_type = field_type


class Field_Type(db.Model, SerializerMixin):  
    __tablename__ = 'field_type'

    serialize_only = ('field_type')
    
    field_type =  db.Column(db.String(10), nullable = False)     
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field = db.relationship('Field', backref='field_type_', lazy=True)

    def __init__(self, field_type):
        self.field_type = field_type
        

@app.route('/', methods=['GET', 'POST'])
def admin():
    return render_template('main.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    users = User.query.order_by(User.id)
    return render_template('user.html', users=users)


@app.route('/remove_user/<string:user_id>', methods=['GET', 'POST'])
def remove_user(user_id):
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('users'))


@app.route('/company', methods=['GET', 'POST'])
def company():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    if request.method == 'POST':
        f = request.files['logo']
        if f.filename != '':
            f.save(dir_path + "\\static\\app-assets\\images\\company_logo\\" + secure_filename(f.filename))
        if request.form['cur_cnpj'] == "---":
            comp = Company(request.form['comp_name'], request.form['cnpj'], request.form['email'], f.filename, request.form['standard_rate'], request.form['improved_rate'])
            db.session.add(comp)
        else:
            db.session.query(Company).filter_by(cnpj = request.form['cur_cnpj']).update({Company.comp_name:request.form['comp_name'], Company.cnpj:request.form['cnpj'], Company.email:request.form['email'], Company.logo:f.filename, Company.standard_rate:request.form['standard_rate'], Company.improved_rate:request.form['improved_rate']}, synchronize_session = False)
            
        db.session.commit()
    companies = Company.query.order_by(Company.comp_name)
    return render_template('company.html', comps=companies)


@app.route('/remove_company/<string:cnpj>', methods=['GET', 'POST'])
def remove_company(cnpj):
    db.session.query(Company).filter_by(cnpj=cnpj).delete()
    db.session.commit()
    return redirect(url_for('company'))


@app.route('/table', methods=['GET', 'POST'])
def table_():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    if request.method == 'POST':
        if request.form['cur_id'] == "---":
            comp = Tbl(request.form['tbl_name'], request.form['description'])
            db.session.add(comp)
        else:
            db.session.query(Tbl).filter_by(id = request.form['cur_id']).update({Tbl.tbl_name:request.form['tbl_name'], Tbl.description:request.form['description']}, synchronize_session = False)            
        db.session.commit()
    tbls = Tbl.query.order_by(Tbl.id)
    return render_template('table.html', tbls=tbls)


@app.route('/remove_table/<string:table_id>', methods=['GET', 'POST'])
def remove_table(table_id):
    db.session.query(Tbl).filter_by(id=table_id).delete()
    db.session.commit()
    return redirect(url_for('table_'))

@app.route('/field', methods=['GET', 'POST'])
def field():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    tbls = Tbl.query.order_by(Tbl.id)
    tbl_id = -1
    if len(tbls.all()) > 0:
        tbl_id = tbls.first().id
    print("tbl_id = " + str(tbl_id))
    return redirect(url_for('field_of_table', tbl_id=tbl_id))

@app.route('/field/<int:tbl_id>', methods=['GET', 'POST'])
def field_of_table(tbl_id):
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    if request.method == 'POST':
        if request.form['cur_id'] == "---":
            comp = Field(request.form['tbl_id'], request.form['from'], request.form['to'], "", request.form['field_type'])
            db.session.add(comp)
        else:
            print(str(request.form['cur_id']))
            db.session.query(Field).filter_by(id = request.form['cur_id']).update({Field.from_:request.form['from'], Field.to:request.form['to'], Field.field_type:request.form['field_type']}, synchronize_session = False)            
        db.session.commit()
    field_types = Field_Type.query.order_by(Field_Type.id)
    tbls = Tbl.query.order_by(Tbl.id)
    # fields = Field.query.order_by(Field.id)
    fields = Field.query.join(Field_Type, Field.field_type==Field_Type.id).add_columns(Field.id, Field.tbl_id, Field.from_, Field.to, Field_Type.field_type).filter(Field.tbl_id==tbl_id)
   
    return render_template('field.html', fields=fields, tbls=tbls, field_types=field_types, tbl_id=tbl_id)


@app.route('/remove_field/<int:field_id>', methods=['GET', 'POST'])
def remove_field(field_id):
    db.session.query(Field).filter_by(id=field_id).delete()
    db.session.commit()
    return redirect(url_for('field'))


@app.route('/rule', methods=['GET', 'POST'])
def rule():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    tbls = Tbl.query.order_by(Tbl.id)
    tbl_id = -1
    if len(tbls.all()) > 0:
        tbl_id = tbls.first().id
    print("tbl_id = " + str(tbl_id))
    return redirect(url_for('rule_of_table', tbl_id=tbl_id))

@app.route('/rule/<int:tbl_id>', methods=['GET', 'POST'])
def rule_of_table(tbl_id):
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    if request.method == 'POST':
        db.session.query(Field).filter_by(id = request.form['cur_id']).update({Field.to:request.form['to'], Field.rule:request.form['rule']}, synchronize_session = False)            
        db.session.commit()
    tbls = Tbl.query.order_by(Tbl.id)
    rules = Field.query.order_by(Field.id).filter(Field.from_=="", Field.tbl_id==tbl_id)
    fields = Field.query.order_by(Field.id).filter(Field.tbl_id==tbl_id)
    # fields = Field.query.join(Field_Type, Field.field_type==Field_Type.id).add_columns(Field.id, Field.tbl_id, Field.from_, Field.to, Field_Type.field_type).filter(Field.tbl_id==tbl_id)
   
    return render_template('rule.html', rules=rules, fields=fields, tbls=tbls, tbl_id=tbl_id)


@app.route('/remove_rule/<int:rule_id>', methods=['GET', 'POST'])
def remove_rule(rule_id):
    db.session.query(Field).filter_by(id=rule_id).delete()
    db.session.commit()
    return redirect(url_for('rule'))

@app.route('/edit_dashboard', methods=['GET', 'POST'])
def edit_dashboard():
    # if not 'username' in session:
    #     return redirect(url_for("login"))
    
    return render_template('edit_dashboard.html')



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
