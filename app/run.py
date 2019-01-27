from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = '0F1CA775123C57D11D66C856DB9807D7453102968CF0F1E2B546056A696D49BC'

bootstrap = Bootstrap(app)
moment = Moment(app)

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
    firstName = None
    lastName = None
    userName = None
    userEmail = None
    userPassword = None
    form = SignupForm()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        userName = form.userName.data
        userEmail = form.userEmail.data
        userPassword = form.userPassword.data
        form.firstName.data = ''
        form.lastName.data = ''
        form.userEmail.data = ''
        form.userName.data = ''
        form.userPassword.data = ''
    return render_template('signup.html', form=form, firstName=firstName, lastName=lastName, userName=userName, userEmail=userEmail, userPassword=userPassword)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500



if __name__ =='__main__':
    app.run(debug=True)

