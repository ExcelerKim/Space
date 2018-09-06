from flask import (Flask,
                   render_template, # render_template_string (특수문자 걸러줌)
                   request,
                   redirect,)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin
from datetime import datetime
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


app = Flask(__name__, template_folder=".")
moment = Moment(app)
db = SQLAlchemy(app)
admin = Admin(app)
GoogleMaps(app)


# config data 는 환경변수에 넣는 것이 일반적 (hacking을 막기 위해서)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '김형석'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyB6kDD37k6cNMf1AX4aRcYbXszWL49JpQE'

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='hskim6543@gmail.com', password='DAN04IEL04')
#     db.session.commit()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

class MyForm(FlaskForm):
    text = StringField('text1', validators=[DataRequired()])
    password = PasswordField('password1')

class SearchForm(FlaskForm):
    search = StringField('검색', validators=[DataRequired()])

@app.route('/')
def index():
    # a = [1,2,3,4,5,6,7,8]
    # b = list('abcdefg')
    # c = list(zip(a,b))
    # d = {'a': 1, 'b': 2, 'c': 3}
    # users = User.query.all()
    now = datetime.utcnow()
    return render_template('index.html', dt=now)


@app.route('/map/')
def mapview():
    # creating a map in the view
    # mymap = Map(
    #     identifier="view-side",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers=[(37.4419, -122.1419)]
    # )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        # markers=[
        #     {
        #         'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        #         'lat': 37.4419,
        #         'lng': -122.1419,
        #         'infobox': "<b>Hello World</b>"
        #     },
        #     {
        #         'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        #         'lat': 37.4300,
        #         'lng': -122.1400,
        #         'infobox': "<b>Hello World from other place</b>"
        #     }
        # ]
    )
    # return render_template('map.html', mymap=mymap, sndmap=sndmap)
    return render_template('map.html', sndmap=sndmap)

@app.route('/a')
def a():
    return 'a' # int 불가
@app.route('/b/') # 주소 뒤에 '/'붙이는 게 더 나음
def b():
    return 'b'

@app.route('/add')
def add():
    user = User() #instance 화
    user.email = 'hskim6543@gmail.com'
    user.username = 'kim'
    db.session.add(user)
    # db.insert(user)
    db.session.commit()
    return render_template('index.html')

# @app.route('/insert')
# def insert():
#     name = request.args.get('name')
#     from pandas_ import pandas_index
#     data = pandas_index(name)
#     data2 = pd.DataFrame(data)
#     data2.to_html('a.html')
#     return render_template('a.html')


# @app.route('/insert')
# def insert():
#     ue = request.args.get('ue') #ue: user_email
#     uu = request.args.get('uu') #uu: user_username
#     user = User()
#     user.email = ue
#     user.username = uu
#     user.id = 1
#     db.session.add(user)
#     db.session.commit()
#     return render_template('index.html')


@app.route('/form', methods=['GET','POST'])
def form1():
    form = MyForm()
    if request.method == 'GET':
        if form.validate_on_submit():
            return render_template('index.html')
        # a = request.args.get('a','') # default 값 지정 가능
        # b = request.args['a']
        # c = request.args.a # (x)
        return render_template('form.html', form2=form)
    else:
        return render_template('form.html', form2=form)


@app.route('/form2', methods=['POST'])
def form2():
    return render_template('form.html')

@app.route('/search',methods=['POST'])
def search():
    search_term = request.form['search']
    # search_term = request.form.get('search')
    if search_term == 'kim':
        return render_template('index.html')
    return redirect('/form')

@app.route('/graph')
def graph():
    # graph 그리는 부분
    from data import plotdata
    script, div = plotdata()
    return render_template('graph.html',script=script, div=div)

# app.add_url_rule
if __name__ == '__main__':
    app.run(debug=True)

# search_url = f'search.daum.net/search?f(search)'