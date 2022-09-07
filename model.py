from re import X
from sqlite3 import dbapi2
from tkinter import Y
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import PrimaryKeyConstraint

#取得目前文件資料夾路徑

pjdir  = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data.sqlite')

db = SQLAlchemy(app)

#繼承稍早所初始化的db.Model
class User(db.Model):
    #__tablename__ = 'User'
    #從原本一對一 變成 一對多所以要改成users
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True , nullable = False)
    X = db.Column(db.Float, unique = False,  nullable = False)
    Y = db.Column(db.Float, unique = False,  nullable = False)
    Z = db.Column(db.Float, unique = False,  nullable = False)


    #set關聯性 relationship設置唯一對多的「一」
    #讓SQLALchemy知道Contact和User是有關連的，前提是要有ForiegnKey
    contacts = db.relationship('Contact', backref = 'user')#,lazy = 'dynamic')
    #和其他class連起來
    #lazy 讓SQLAlchemy在搜尋關聯資料的時候保留物件狀態
    '''
    def __init__(self, username, email) :
        self.username = username
        self.email = email
    '''
    
    def __repr__(self):
        return '<User %r>' % self.username
print('====接下來就要到python shell建資料庫====')
print('====建完了現在要一對多====')


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    #SQLAlchemy中，每個Model都要求要設置主鍵，名稱通常設置為id
    contact_style = db.Column(db.String)
    contact_context = db.Column(db.String)
    #set 外來鍵 ForeignKey設置在一對多的「多」
#以資料庫的角度去看，這代表我們在保存聯絡方式的時候會在資料庫內存儲使用者的IDusers.id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) :
        return 'contact_style:%s , contact_context:%s ' % \
            (self.contact_style , self.contact_context)

#將資料寫入資料庫
'''
jam = User(username = 'jam', email = 'jam@gmail.com')
contact = Contact(contact_style = 'email', contact_context = 'jam3@gmail.com')
jam.contacts.append(contact)
db.session.add(jam)
db.session.commit()

try:
    db.session.commit()
except :
    db.session.rollback()
    raise
finally:
    db.session.close()
'''
#print('已經新增tommy一對多contact進入資料庫')

#另一種關聯寫入資料的方式
#打在SHELL