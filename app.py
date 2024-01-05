# Import necessary libraries
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# Run source/venv/bin/activate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret'
Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember_session = BooleanField('Remember session')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

# ------------------
# Route to home page
@app.route('/')
def home_page():
    return render_template('index.html')

# -------------------
# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        return '<h1> Welcome ' + form.username.data + '</h1>'
        return render_template('dashboard.html')
    return render_template('login.html', form=form)

# -------------------
# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    return render_template('signup.html', form=form)

# -------------------
# Route for dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ---------------------------
if __name__ == "__main__":
    config()
    app.run(debug=True)
