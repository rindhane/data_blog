#references : 
#https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/cloud-sql/mysql/sqlalchemy
#https://cloud.google.com/sql/docs/mysql/connect-app-engine
#https://www.youtube.com/watch?v=QEMtSUxtUDY&t=1s
#https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/flexible/cloudsql/main.py


#issues to handle : 
#use primaryKey 'variable' 
#where to keep schema
# see if fetch one can be replaced by fetchall in single item retrieval >> check the correnction line

from flask import Flask, render_template,flash, redirect, url_for, session, request, logging
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
from passlib.hash import sha256_crypt
from functools import wraps
#from data import Articles
from sqlalchemy import text
from utilities import logger, environ, checkKey, SCHEMA
from database_connector_new import get_items,\
                                insert_item,\
                                update_item,\
                                delete_item                                    

app= Flask(__name__)
app.secret_key=environ.get("SECRET_KEY")

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
    articles=get_items(table='ARTICLES')
    if len(articles)>0:
        return render_template("articles.html",articles=articles)
    else:
        msg="No Articles Found"
        return render_template("articles.html", msg=msg)

#single article
@app.route("/Articles/<int:idx>/")
def article(idx):
    article=get_items(table='ARTICLES', 
                            where={SCHEMA['tables']['ARTICLES'][checkKey]: idx}
                        )
    if len(article)>0:
        return render_template("article.html", article=article[0]) #check if this correction is ok
    else:
        msg="No Article Found"
        return render_template("article.html", msg=msg)

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
        registration="close" #variable to shut-off the registration entries
        #passing the registration details in to the database entries 
        if registration =="open":
            insert_item(
                         table='USERS',
                          insert={
                                SCHEMA['tables']['USERS']['fields'][0]:name,
                                SCHEMA['tables']['USERS']['fields'][1]:email,
                                SCHEMA['tables']['USERS']['fields'][2]:username,
                                SCHEMA['tables']['USERS']['fields'][3]:password,
                                }
                        )
            #new user is inserted in to the database.
        flash ("You are now registered user and can log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

#User Login
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        #get form fields
        username = request.form["username"]
        password_candidate = request.form["password"]
        # Get user by username
        temp=get_items(table="USERS", 
                        where={
                        SCHEMA['tables']["USERS"][checkKey]: username}
                        )
        #print(temp)
        #print(SCHEMA['tables']["USERS"][checkKey],",", username) 
        if len(temp) > 0: 
            #get stored hash
            data = temp[0]
            password =data["password"]
            #print(sha256_crypt.verify(password_candidate,password))
            if sha256_crypt.verify(password_candidate,password):
                #passed authentication
                session["logged_in"]= True
                session["username"]=username
                #show message of logging in 
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
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for("login"))

#Dashboard
@app.route("/dashboard")
@is_logged_in
def dashboard():
    articles=get_items(table='ARTICLES')
    if len(articles)>0:
        return render_template("dashboard.html",articles=articles)
    else:
        msg="No Articles Found"
        return render_template("dashboard.html", msg=msg)

class ArticleForm(Form):
    title= StringField("title", [validators.Length(min=1, max=200)])
    body=TextAreaField("body",[validators.Length(min=30)])
    
#view for add_arcticle
@app.route("/add_article", methods=["GET", "POST"])
@is_logged_in
def add_article():
    form =ArticleForm(request.form)
    if request.method =="POST" and form.validate():
        title=form.title.data
        body=form.body.data
        #excute into the database
        insert_item(
            table='ARTICLES',
            insert={
            SCHEMA['tables']['ARTICLES']['fields'][0]:title,
            SCHEMA['tables']['ARTICLES']['fields'][1]:body,
            SCHEMA['tables']['ARTICLES']['fields'][2]:session["username"],
            })
        #it gets auto-commited &closing the connection
        #success message
        flash("Article Created","success")
        #redirecting to dashboard
        return redirect(url_for('dashboard'))
    return render_template('add_article.html',form=form)

@app.route("/edit_article/<int:idx>", methods=["GET", "POST"])
@is_logged_in
def edit_article(idx):
    #check if any article with that id exist
    article= get_items(table='ARTICLES',
             where= {
             SCHEMA['tables']['ARTICLES'][checkKey]: idx 
             })
    if article == list():
        msg="No Article Found"
        flash(msg,"danger")
        return redirect(url_for("articles"))
    #create new form
    form =ArticleForm(request.form)
    #write action for POST METHOD of FORM  
    if request.method =="POST" and form.validate():
        title=request.form["title"]
        body=request.form["body"]
        #call database function to execute the details and execute to enter the details
        #print(title,body,session["username"])
        update_item(table="ARTICLES",
                    set_items={
                    SCHEMA['tables']['ARTICLES']['fields'][0]:title,
                    SCHEMA['tables']['ARTICLES']['fields'][1]:body,
                    SCHEMA['tables']['ARTICLES']['fields'][2]:session["username"],
                    },
                    where={
                        SCHEMA['tables']['ARTICLES'][checkKey]: idx 
                        },
                    )
        #success message
        flash("Article updated","success")
        #redirecting to dashboard
        return redirect(url_for('dashboard'))
    #action for GET method  
    #populate article form fields
    article=article[0]
    form.title.data=article["title"]
    form.body.data=article["body"]
    #based on available form render the result
    return render_template('edit_article.html',form=form)

#Delete Article
@app.route('/delete_article/<int:idx>', methods=["POST"])
@is_logged_in
def delete_article(idx):
    #Execute
    delete_item(table='ARTICLES',
             where= {
             SCHEMA['tables']['ARTICLES'][checkKey]: idx 
             })
    flash('Article got deleted','success')
    return redirect(url_for("dashboard"))

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)