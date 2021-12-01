from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, RadioField, DateField, TimeField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets.core import PasswordInput
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
db = SQLAlchemy(app)
STATE_ABBREV = ('5','10','15','20','25','30','35','40','45','50','55','60')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'ghghchgcghchhddgdgf'
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class DataFetch(FlaskForm):
    start_date = DateField('Start Date', format='%m/%d/%Y')
    date = DateField('Date', validators=[InputRequired(), Length(min=4, max=15)])
    time = TimeField('password', validators=[InputRequired(), Length(min=8, max=80)])
    period = SelectField(label='period',   choices=[(state, state) for state in STATE_ABBREV])



@app.route('/', methods=['GET', 'POST'])
def login():
    print(request.method)
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        print(username, password)
        if username == "adit" or password:
                
            return redirect(url_for('dashboard'))

    elif request.method == 'GET':

        return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("here")
    form = DataFetch()
    if request.method == 'POST':
        
        return render_template('Co-ordinates.html', form=form)
    
    elif request.method == 'GET':

        return render_template('Co-ordinates.html', form=form)    

if __name__ == '__main__':
    app.run(debug=True)