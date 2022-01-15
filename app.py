from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# dataabse uses CRUD (create, read, update, delete)
file_path = os.path.abspath(os.getcwd())+"/database.db"


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title} - {self.desc}'


# render template is used to render the files from template folder like index.html


@ app.route('/', methods=['GET', 'POST'])
def hello_wrold():
    if (request.method == 'POST'):
        title = request.form['title']
        desc = request.form['desc']
        if len(title) == 0 or len(desc) == 0:
            print('Nothing to Pass')
        else:
            todo = ToDo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = ToDo.query.all()
    # rendering template uses jinja2 for passing python varibles
    return render_template('index.html', allTodo=allTodo)


@ app.route('/products')
def products():
    return 'this is product page'


@app.route('/show')
def show():
    allTodo = ToDo.query.all()
    return render_template('show.html', allTodo=allTodo)


@app.route('/delete/<int:sno>')
def delete_record(sno):
    record = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/modify/<int:sno>', methods=['GET', 'POST'])
def modify_record(sno):

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('modify.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
