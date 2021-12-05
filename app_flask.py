from flask import Flask, render_template, redirect, url_for,request, session, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, RadioField, DateField, TimeField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets.core import PasswordInput
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, url_for,request, send_file, session
from flask.sessions import NullSession
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
import sqlite3
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
    

app = Flask(__name__)

STATE_ABBREV = ('5','10','15','20','25','30','35','40','45','50','55','60')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'ghghchgcghchhddgdgf'
class LoginForm(FlaskForm):
    devise_id = StringField('Device ID', validators=[InputRequired(), Length(min=1, max=15)])

class DataFetch(FlaskForm):
    start_date = DateField('Start Date', format='%m/%d/%Y')
    date = DateField('Date', validators=[InputRequired(), Length(min=4, max=15)])
    time = TimeField('Time', validators=[InputRequired(), Length(min=8, max=80)])
    period = SelectField(label='period',   choices=[(state, state) for state in STATE_ABBREV])



@app.route('/', methods=['GET', 'POST'])
def login():
    print(request.method)
    form = LoginForm()
    if request.method == 'POST':
        devise_id = form.devise_id.data
        print(devise_id)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        check = c.execute("SELECT * FROM member WHERE Device_ID =?",(devise_id,))
        check = c.fetchall()
        print(check)
        if len(check) ==0:
            return render_template("login.html", form=form, message = "Please start up the devise")
        
        session["devise_id"] = devise_id
        return redirect(url_for('dashboard'))

    elif request.method == 'GET':

        return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("here")
    form = DataFetch()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    last_row = c.execute('select * from member WHERE Device_ID =?',(session["devise_id"] ,)).fetchall()[-1] 
    print(last_row)
    headings = ("device_id", "date_time", "GPS_lat", "GPS_long","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z") 
    html = str('https://maps.google.com/maps?q='+str(last_row[3])+","+str(last_row[4]))
    if request.method == 'POST':
        date = form.date.data
        time = form.time.data
        period = form.period.data
        print(date, time, period)
        
        date = ''.join(filter(str.isalnum, str(date)) )
        time = ''.join(filter(str.isalnum, str(time)) )[: -2]
        # time_period = int(time)+  
        start = date+time
        print(int((int(time[-2 :])+int(period))/60)*100 + int((int(time[-2 :])+int(period))%60) )
        time_period = str(int((int(time[-2 :])+int(period))/60)*100 + int(time))[: -2]+ str((int(time[-2 :])+int(period))%60) 
        print(time_period)
        end= date+str(time_period)
        print(start, end)
        session["start"] = start
        session["end"] = end



        return redirect(url_for('history'))
    
    elif request.method == 'GET':

        return render_template('Co-ordinates.html', form=form    ,x=last_row[3], y=last_row[4], html=html )



@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("select * from member")
        rows1 = (c.fetchall())
        print(session["devise_id"], session["start"],session["end"] )
        c.execute("SELECT * FROM member WHERE  Device_ID = ? and date_time between ? and ?",( session["devise_id"], session["start"],session["end"] ,))
      
        rows = (c.fetchall())
        headings = ("device_id", "date_time", "GPS_lat", "GPS_long","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z") 
        conn.close()
        print(rows1)

        return render_template('history.html', rows = rows, heading= headings)

@app.route('/in_out_api', methods=['GET', 'POST'])
def in_out_api():
    GPS_lat = request.args.get('GPS_lat')
    GPS_long = request.args.get('GPS_long')
    acc_x = request.args.get('acc_x')
    acc_y = request.args.get('acc_y')
    acc_z = request.args.get('acc_z')
    gyro_x = request.args.get('gyro_x')
    gyro_y = request.args.get('gyro_y')
    gyro_z = request.args.get('gyro_z')
    device_id = request.args.get('devise_id')
    date_time  = ''.join(filter(str.isalnum, str(datetime.now())) )[: -8]
    print(device_id, date_time,GPS_lat, GPS_long,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()


    c.execute("INSERT INTO member VALUES (?,?,?,?,?,?,?,?,?,?) ", (device_id, date_time,GPS_lat, GPS_long,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z))
    conn.commit()
    new_cord  = (device_id, date_time,GPS_lat, GPS_long,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z)
    
    conn.close()
 

    return "received"

@app.route("/change")
def change():
    ID = request.args.get('ID')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    new_cord  = ("device_id", "date_time","GPS_lat", "GPS_long","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z")
    try:
        row = c.execute('select * from member WHERE Device_ID =?',(str(ID),)).fetchall()
        last_row = row[-1]
        second_last = row[-2]

    except:
        return jsonify(())
    out = {}
    for index, value in enumerate(new_cord):
        out[value] = last_row[index]

    
    if last_row == second_last:
        out["is_changed"] = "NO"
    else:
        out["is_changed"] = "YES"
    return jsonify(out)


    
if __name__ == '__main__':

    # conn = sqlite3.connect('database.db')
    # print ("Opened database successfully")
    # c = conn.cursor()
    # c.execute("""CREATE TABLE member (Device_ID TEXT,date_time INTEGER, GPS_lat TEXT, GPS_long TEXT,acc_x TEXT, acc_y TEXT, acc_z TEXT, gyro_x TEXT,gyro_y TEXT, gyro_z TEXT)""")
    # conn.commit
    # conn.close()
    


    app.run(debug=True, port=3000)
 