import email
from flask import Flask
from flask import Flask, render_template, url_for, request, flash, abort, redirect
import sqlite3
import pandas as pd
import csv
import os
import time
from model_predict import vibration_preprocess,predict
from model_output_plot import model_ouput_plot

app = Flask(__name__)  # 物件類別給他一個名字 後實體化wth
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/' ,methods=['GET','POST'], strict_slashes=False)
def firstpage():
    return render_template('first_page.html')

@app.route('/homepage.html')
def homepage():
    conn = get_db_connection('signin.db') # 從signin db 取資料
    data = conn.execute('SELECT * FROM signin').fetchall() # 歡迎XXX的資料
    conn.commit()
    conn.close()

    conn2 = get_db_connection('base.db') # base db 取資料
    sleep_data = conn2.execute('SELECT * FROM base').fetchall() #睡了多久、深淺眠%數等等資料
    conn2.commit()
    conn2.close()
    return render_template('homepage.html',data=data,sleep_data=sleep_data) 
# 首頁超連結


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/start.html', methods=['GET', 'POST'])  # 如何開始介面
def start():
    return render_template('start.html')


@app.route('/introduction.html')  # 專案介紹介面
def introduction():
    return render_template('introduction.html')

@app.route('/problem.html') # 常見問題介面
def problem():
    return render_template('problem.html')


@app.route('/sleepClassroom.html') # 睡眠小學堂介面
def sleepClassroom():
    return render_template('sleepClassroom.html')

@app.route('/upload.html', methods=('GET', 'POST') ) # 上傳資料介面
def upload():
    conn = get_db_connection('signin.db')
    data = conn.execute('SELECT * FROM signin').fetchall()
    conn.commit()
    conn.close()
    return render_template('upload.html',data=data) #data要看html js

@app.route('/feedback.html', methods=['GET', 'POST'] , strict_slashes=False)
def feeback():
    conn = get_db_connection('signin.db')
    data = conn.execute('SELECT * FROM signin').fetchall()
    conn.commit()
    conn.close()
    return render_template('feedback2.html',data=data)

@app.route('/signin_create2' , methods=('GET','POST'))
def signin_create2():
    if request.method == 'POST':
        q1 = f"'{request.form['q1']}'"
        q2 = f"'{request.form['q2']}'"
        opinion = f"'{request.form['opinion']}'"
        conn = get_db_connection('feedback.db')
        conn.execute(f'INSERT INTO feedback (q1,q2,opinion) VALUES ({q1},{q2},{opinion})')
        conn.commit()
        conn.close()

        conn2 = get_db_connection('signin.db')
        data = conn2.execute('SELECT * FROM signin').fetchall()
        conn2.commit()
        conn2.close()
    return render_template('feedback2.html',data = data)

def get_db_connection(db): # 連結資料庫function
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signin_create', methods=('GET', 'POST')) # 登入介面
def signin_create():
    if request.method == 'POST':
        username = f"'{request.form['username']}'" #username來自html form的input(加單引號變字串)
        email = f"'{request.form['email']}'" #email也來自html form的input
        conn = get_db_connection('signin.db') # 取sigin.db資料
        conn.execute(f'INSERT INTO signin (username,email) VALUES ({username},{email})')
        data = conn.execute('SELECT * FROM signin').fetchall()
        conn.commit()
        conn.close()

        conn2 = get_db_connection('base.db') # 取base.db資料
        sleep_data = conn2.execute('SELECT * FROM base').fetchall()
        conn2.commit()
        conn2.close()
    return render_template('homepage.html',data = data,sleep_data=sleep_data)


@app.route('/create', methods=('GET', 'POST'))
def create(deep_sleep,light_sleep,sleep_time,sleep_status): # 定義post資料function
    if request.method == 'POST':
        conn1 = get_db_connection('base.db')
        conn1.execute(f"INSERT INTO base (deep_sleep, light_sleep, sleep_time, sleep_status) VALUES ({deep_sleep},{light_sleep},'{sleep_time}','{sleep_status}' )")
        conn1.commit()
        conn1.close()
    return "OK"


###### 上傳csv(重點部分) ######
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['csv'])  # 允许上传的文件后缀

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/data', methods=['POST'], strict_slashes=False) # csv上傳介面
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f=request.files['csvfile']  # 从表单的file字段获取文件，csvfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        # fname=f.filename
        # ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        # unix_time = int(time.time())
        # new_filename = str(unix_time)+'.'+ext   # 修改文件名
        f.save(os.path.join(file_dir, "origin.csv"))  #保存文件到upload目录

        final_data=vibration_preprocess(f"{file_dir}/origin.csv") # 接資料處理
        predict_output = predict(final_data) # 接模型輸出predict
        df = pd.DataFrame(predict_output)
        df.to_csv(f'{file_dir}/final_data/output.csv') #儲存最後的output.csv
        sleep_time = df['Total Sleep Time'][0] #讀取output.csv
        light_sleep = int(df['Light Sleep Probability(%)'][0]) #讀取output.csv
        deep_sleep = int(df['Deep Sleep Probability(%)'][0]) #讀取output.csv
        if deep_sleep >= 20:
            sleep_status = '睡得很好'
        elif deep_sleep < 20 and deep_sleep >= 10:
            sleep_status = '睡得普通'
        else:
            sleep_status = '睡得不好'

        create(deep_sleep,light_sleep,sleep_time,sleep_status) # 發post到base.db
        model_ouput_plot(input_path="upload/final_data/output.csv",output_path="static/images",second_interval=60*20) # 接畫圖


        return render_template('upload_success.html')# 上傳成功字顯示
    else:
        return "上傳失敗 "

@app.route('/index')
def index():
    data= {'nickname': 'Miguel'} # fake user
    return render_template("test.html",data = data)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)