from flask import Flask, render_template
from data import Articles
app= Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/Articles")
def articles():
    return render_template("articles.html", articles=Articles())

@app.route("/Articles/<string:id>/")
def article(id):
    return render_template("article.html", id=id)



if __name__=="__main__":
    app.run(debug=True)