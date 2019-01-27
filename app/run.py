import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '0F1CA775123C57D11D66C856DB9807D7453102968CF0F1E2B546056A696D49BC'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.rolename

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    firstname = db.Column(db.String(20), unique=False)
    lastname = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(60), unique=True)
    userpassword = db.Column(db.Text)
    datecreated = db.Column(db.DateTime)
    lastlogin = db.Column(db.DateTime)
    lastlogout = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    def __repr__(self):
        return '<User %r>' % self.firstname

class Questions(db.Model):
    __tablename__ = 'questions'
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    quizasked = db.Column(db.Text)
    quizstatus = db.Column(db.Integer)
    answer_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Questions %r>' % self.quizasked

class Answers(db.Model):
    __tablename__ = 'answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    quizanswer = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    votes_up = db.Column(db.Integer)
    votes_down = db.Column(db.Integer)

    def __repr__(self):
        return '<Answers %r>' % self.quizanswer

class Edits(db.Model):
    __tablename__ = 'edits'
    edit_id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    quizedit = db.Column(db.Text)
    date_edited = db.Column(db.DateTime)

    def __repr__(self):
        return '<Edits %r>' % self.quizedit

class Login(db.Model):
    __tablename__ = 'logins'
    login_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    logintime = db.Column(db.DateTime)
    logouttime = db.Column(db.DateTime)

    def __repr__(self):
        return '<Login %r>' % self.login_id


class SignupForm(FlaskForm):
    firstName = StringField('First Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    userName = StringField('Username(Optional):', validators=[Optional()])
    userEmail = StringField('Email:', validators=[Email(),DataRequired()])
    userPassword = PasswordField('Password:', validators=[DataRequired(),Length(8)])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    # firstName = None
    # lastName = None
    # userName = None
    # userEmail = None
    # userPassword = None
    form = SignupForm()
    if form.validate_on_submit():
        useravailable = User.query.filter_by(userEmail=form.userEmail.data).first()
        if useravailable is None:
            useravailable = User(userEmail=form.userEmail.data)
            firstname = User(firstName=form.firstName.data)
            lastname = User(lastName=form.lastName.data)
            username = User(userName=form.userName.data)
            userpassword = User(userPassword=form.userPassword.data)
            db.session.add_all([useravailable, firstname, lastname, username, userpassword])
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['firstName'] = form.firstName.data
        session['lastName'] = form.lastName.data
        session['userName'] = form.userName.data
        session['userEmail'] = form.userEmail.data
        session['userPassword'] = form.userPassword.data
        # form.firstName.data = ''
        # form.lastName.data = ''
        # form.userEmail.data = ''
        # form.userName.data = ''
        # form.userPassword.data = ''
        return redirect(url_for('signup'))
    return render_template('signup.html', form=form, firstName=session.get('firstName'), lastName=session.get('lastName'), userName=session.get('userName'), userEmail=session.get('userEmail'), userPassword=session.get('userPassword'), known=session.get('known', False))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500



if __name__ =='__main__':
    app.run(debug=True)

