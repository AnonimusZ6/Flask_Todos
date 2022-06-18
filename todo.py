from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dtabbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intr = db.Column(db.String(30), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return "<ToDos %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        Intro = request.form['intro']
        Text = request.form['text']

        worst = Database(intr=Intro, text=Text)

        try:
            db.session.add(worst)
            db.session.commit()
            return redirect('/listofdo')
        except:
            return "При добавлении произошла ошибка"

    else:
        return render_template("create.html")


@app.route("/listofdo")
def lst():
    todoss = Database.query.order_by(Database.date.desc()).all()
    return render_template("listofdo.html", todd = todoss)


if __name__ == "__main__":
    app.run(debug=True)


