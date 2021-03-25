
from faker import Faker
from flask import Flask, redirect, url_for, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


fake = Faker()

DATABASE = "users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'User number {} with name {} & email {}\n'.format(self.id, self.name, self.email)



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/users/all")
def users_all():
    users = [
        dict(id=users.id, name=users.name, email=users.email)
        for users in db.session.query(User).all()
    ]
    return jsonify(users)


@app.route("/users/gen")
def users_gen():
    usr = User(name=fake.name(), email=fake.email())
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/delete-all")
def users_del_all():
    for obj in db.session.query(User).all():
        db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/count")
def users_count():
    quantity = 0
    for _ in db.session.query(User).all():
        quantity += 1
    return jsonify({"the quantity of users": quantity})



@app.route("/users/add", methods=['GET', 'POST'])
def users_add():
    if request.method == "GET":
        return render_template("user_add.html")
    else:
        temp_name = request.form["user_name"]
        temp_email = request.form["email"]
    temp_user = User(name=temp_name, email=temp_email)
    db.session.add(temp_user)
    db.session.commit()
    return redirect(url_for('users_all'))


if __name__ == "__main__":
    app.run(debug=True)

