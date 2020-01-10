#references : 
#https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/cloud-sql/mysql/sqlalchemy
#https://cloud.google.com/sql/docs/mysql/connect-app-engine
#https://www.youtube.com/watch?v=QEMtSUxtUDY&t=1s
#https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/flexible/cloudsql/main.py


from flask import Flask, render_template,flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
from passlib.hash import sha256_crypt
from functools import wraps
from data import Articles
import sqlalchemy
import os 
import logging

app= Flask(__name__)

app.secret_key=os.environ.get("SECRET_KEY")
string_local=os.environ.get("db_localhost")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
logger=logging.getLogger()

mode="cloud"
if mode =="local": 
    db=sqlalchemy.create_engine(string_local)
else :     
    db= sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket":"/cloudsql/{}".format(cloud_sql_connection_name)},
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,

    )


#Config MySQL
#app.config["MYSQL_HOST"]="localhost"
#app.config["MYSQL_USER"]="root"
#app.config["MYSQL_PASSWORD"]="trial@123"
#app.config["MYSQL_DB"]="myflaskapp"
#app.config["MYSQL_CURSORCLASS"]="DictCursor"
#init MYSQL
#mysql=MySQL(app)

#index
@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html")

#about page
@app.route("/about")
def about():
    return render_template("about.html")

#Articles
@app.route("/Articles")
def articles():
    return render_template("articles.html", articles=Articles())

#single article
@app.route("/Articles/<string:id>/")
def article(id):
    return render_template("article.html", id=id)

#Registeration Form class
class RegisterForm(Form):
    name= StringField("Name", [validators.Length(min=1, max=50)])
    username=StringField("Username",[validators.Length(min=4, max=50)])
    email= StringField("Email", [validators.Length(min=6,max=50)])
    password=PasswordField("Password", [
         validators.DataRequired(),
         validators.EqualTo("confirm", message="Passwords do not match")
    ])
    confirm= PasswordField("Confirm Password")
    
#user registeration form
@app.route("/register", methods=["GET","POST"])
def register():
    form=RegisterForm(request.form)
    if request.method =="POST" and form.validate():
        name= form.name.data
        email=form.email.data
        username=form.username.data
        password =sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        #cur = db.connect()
        registration="close"
        if registration =="open":
            with db.connect() as curr:
                #execute  query 
                curr.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", 
                (name, email, username, password) )
            #Commit to DB
            #mysql.connection.commit()
            #Close connection
            #cur.close()

        flash ("You are now registered user and can log in", "success")
        
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

#helper_function for wrapping string in one more layer of quotes
def quote_string(string):
    string='"'+string+'"'
    return string


#User Login
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        #get form fields
        username = request.form["username"]
        password_candidate = request.form["password"]

        #create cursor 
        curr =db.connect()

        # Get user by username 
        result = curr.execute("SELECT * FROM users WHERE username= {0}".format(quote_string(username)))
        temp=result.fetchall()
        result.close()

        if len(temp) > 0: 
            #get stored hash
            data = temp[0]
            password =data["password"]
        
            if sha256_crypt.verify(password_candidate,password):
                #passed authentication
                session["logged_in"]= True
                session["username"]=username

                flash ("You are now logged in","success")
                return redirect(url_for("dashboard"))
                
            else: 
                error="Invalid login"
                return render_template("login.html", error=error)
        else:
            error="Username not found"
            return render_template("login.html", error=error)


    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", 'danger')
            return redirect(url_for('login'))
    return wrap



@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for("login"))

#Dashboard
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template("dashboard.html")



if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)