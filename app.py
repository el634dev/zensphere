# Import necessary libraries
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from models import LoginForm, User, RegisterForm, db, login_man
from flask_sqlalchemy import SQLAlchemy
# from passlib.hash import pbkdf2_sha256
from flask_login import login_required, login_user
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
Bootstrap(app)

db.init_app(app)
login_man.init_app(app)

# ------------------
# Route to home page
@app.route('/')
def home_page():
    return render_template('index.html')

# -------------------
# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
        # return '<h1>Welcome ' + form.username.data + '</h1>
    return render_template('signup.html', form=form)

# -------------------
# Route for FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# ------------------
# Route for Features page
@app.route('/features')
def features():
    return render_template('features.html')

# -------------------
# Route for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------------------
# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember_session.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
        # return '<h1> Welcome ' + form.username.data + '</h1>'
    return render_template('login.html', form=form)


# --------------------
# Route for chatroom
@app.route("/chatroom")
def chatroom():
    return render_template("chatroom.html")

# ---------------------------
if __name__ == "__main__":
    app.run(debug=False)
