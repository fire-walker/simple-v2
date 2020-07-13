from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
import json
from post import post_blueprint
import itertools

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from passlib.totp import TOTP
import passlib.exc as passlib_errors
import pyqrcode


app = Flask(__name__, static_url_path='/static')
app.register_blueprint(post_blueprint)
app.secret_key = b'somethingl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    totp_enabled = db.Column(db.Boolean, nullable=False, default=False)
    totp = db.Column(db.String, nullable=False, default=False)
    totp_counter = db.Column(db.Integer, nullable=False, default=False)
    
    def help(self):
        print("""
    # create new user
    self.new_user() 

    # set new password
    self.set_pw('password')   

    # check a user's password
    self.check_pw('password')
    
    # generate totp creds
    self.gen_totp()

    # generate user's totp qr
    self.get_totp_qr()

    # check user's totp creds   
    self.auth_verify('int_token')
    """)
    
    def new_user(self):
        self.username = input('Enter username: ')
        self.password = input('Enter password: ')
        totp = input('Two factor auth (y, n)?: ')
        if totp.lower() == 'y':
            self.totp_enabled = True
            
            totp_factory = TOTP.using(secrets_path='totp_sec', issuer='sec.thelonelylands.com')
            totp = totp_factory.new()
            self.totp = json.dumps(totp.to_json())
            uri = totp.to_uri(label=self.username)
            
            input('Please enlarge your screen and press enter')
            print(pyqrcode.create(uri).terminal(quiet_zone=1))
            print("Alternatively: " + totp.pretty_key())
            
            token = input('Enter token to verify: ')
            verification = self.auth_verify(token)
            if verification:
                print('Successfully created user')
                return self
            else:
                print('User creation failed')
                return 
        else:
            print('Successfully created user')
            return self
            
            
            
    def set_pw(self, password):
        self.password = generate_password_hash(password)

    def check_pw(self, password):
        return check_password_hash(self.password, password)

    def gen_totp_qr(self):
        totp_factory = TOTP.using(secrets_path='totp_sec', issuer='sec.thelonelylands.com')
        totp = totp_factory.from_source(json.loads(self.totp))
        uri = totp.to_uri(label=self.username)
        
        input('Please enlarge your screen and press enter.')
        print(pyqrcode.create(uri).terminal(quiet_zone=1))
        print("Alternatively: " + totp.pretty_key())

    def gen_totp(self):
        totp_factory = TOTP.using(secrets_path='totp_sec', issuer='sec.thelonelylands.com')
        totp = totp_factory.new()
        self.totp = json.dumps(totp.to_json())
        uri = totp.to_uri(label=self.username)
        
        input('Please enlarge your screen and press enter.')
        print(pyqrcode.create(uri).terminal(quiet_zone=1))
        print("Alternatively: " + totp.pretty_key())

    def auth_verify(self, token):
        try:
            int(token)
        except ValueError:
            return False
        else:
            token = int(token)

        totp_factory = TOTP.using(secrets_path='totp_sec', issuer='sec.thelonelylands.com')
        source = totp_factory.from_source(json.loads(self.totp))
        
        try:
            verify = TOTP.verify(token=token, source=source, last_counter=self.totp_counter, window=10)
        except (passlib_errors.UsedTokenError, 
                passlib_errors.InvalidTokenError, 
                passlib_errors.MalformedTokenError):
            return False
        else: 
            self.totp_counter = verify.counter
            return True
        
    def __repr__(self):
        return f'({self.id}, {self.username})'


# class Posts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
    
#     totp_enabled = db.Column(db.Boolean, nullable=False, default=False)
#     totp = db.Column(db.String, nullable=False, default=False)
#     totp_counter = db.Column(db.Integer, nullable=False, default=False)
        
#     def __repr__(self):
#         return f'({self.id}, {self.username})'  

    
    
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 
      
      
class TwofaForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Verify') 
    

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', page_title='Page Not Found')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    
    error = False
    if request.args.get('e') == 'otp':
        error = 'Authentification Failed'
            
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if not user or username == '' or password == '' or not check_password_hash(user.password, password):
            error = 'You have entered an invalid username or password'
        else:
            if user.totp_enabled:                
                session['id'] = user.id
                return redirect('/twofactor')
            else:            
                login_user(user)
                return redirect('/')

    
    return render_template('login.html', page_title='Sign In', form=form, error=error)


@app.route('/twofactor', methods=['GET', 'POST'])
def twofactor():  
    try:
        session['id']
    except:
        return redirect('/login?e=otp')

    if current_user.is_authenticated:
        return redirect('/')
    
    form = TwofaForm()
    if form.is_submitted():
        token = form.token.data
        user = User.query.filter_by(id=session['id']).first() 
        auth = user.auth_verify(token)
        del session['id']
        if auth:
            login_user(user)
            return redirect('/')  
        else:
            return redirect('/login?e=otp')
    
    return render_template('login2fa.html', page_title='Sign In', form=form)


@app.route('/forgotpass')
def forgot_pass():
    return render_template('forgotpass.html', page_title='Wonderful!!')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    return redirect('/page?n=1')


@app.route('/page')
def page():
    per_page = 5
    cur_page = int(request.args.get('n'))

    with open('static/posts.json', "r") as file:
        post_data = {int(x): y for x, y in json.load(file).items()}
        page_num = len(post_data.keys()) // per_page
        
    if cur_page > page_num + 1 or cur_page <= 0:
        return render_template('404.html', page_title='Page Not Found')


    page_start = (per_page * cur_page) - per_page
    page_end = (per_page * cur_page)
    post_data = dict(itertools.islice(post_data.items(), page_start, page_end))
    
    if current_user.is_authenticated:
        logged = True
    else:
        logged = False

    return render_template('index.html', page_title='Simple - Index', posts=post_data, page=cur_page, page_tot=page_num, logged=logged)


@app.route('/tags')
def tags():
    with open('static/posts.json', "r") as file:
        post_data = {int(x): y for x, y in json.load(file).items()}

    with open('static/tags.json', "r") as file:
        tag_data = json.load(file)

    return render_template('tags.html', page_title='Simple - Tags', posts=post_data, tags=tag_data)


@app.route('/archive')
def archive2():
    with open('static/posts.json', "r") as file:
        post_data = {int(x): y for x, y in json.load(file).items()}

    return render_template('archive_2.html', page_title='Simple - Archive', posts=post_data)


# @app.route('/archive-3')
# def archive3():
#     something = {

#         1: 'first',
#         2: 'second',
#         3: 'third',
#         4: 'fourth'
#     }
#     return something


@app.route('/editor')
@login_required
def editor():
    with open('static/tags.json', "r") as file:
        tag_data = json.load(file)

    return render_template('editor.html', page_title='Simple - Editor', tags=tag_data)


if __name__ == '__main__':
    app.run(debug=True)
