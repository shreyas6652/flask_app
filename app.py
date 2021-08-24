from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)

db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Age = db.Column(db.String(500), nullable=False)
    Mobile = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Name}"


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        Name=request.form['Name']
        Age=request.form['Age']
        Mobile=request.form['Mobile']
        todo=Todo(Name=Name,Age=Age,Mobile=Mobile)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)



@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        Name=request.form['Name']
        Age=request.form['Age']
        Mobile=request.form['Mobile']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.Name=Name
        todo.Age=Age
        todo.Mobile=Mobile
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
if __name__=='__main__':
    app.run(debug=True)