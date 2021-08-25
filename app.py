from flask import Flask,jsonify
from flask_restful import Api,Resource,fields, marshal_with,reqparse
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=True)
    Age = db.Column(db.String(500), nullable=True)
    Mobile = db.Column(db.String(500), nullable=True)

    def __ref__(self):
        return f"Todo(Name= {Name} ,Age= {Age} ,Mobile= {Mobile})"

resource_fields={
    'sno':fields.Integer,
    'Name':fields.String,
    'Age':fields.Integer,
    'Mobile':fields.String
}
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("Name", type=str, required=True)
video_put_args.add_argument("Age", type=str, required=True)
video_put_args.add_argument("Mobile", type=str,  required=True)

class GetTable(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result=Todo.query.all()
        jsonobj=[]
        for itr in result:
            jsonitr={
                "sno":itr.sno,
                "Name":itr.Name,
                "Age":itr.Age,
                "Mobile":itr.Mobile
            }
            jsonobj.append(jsonitr)
        return(jsonobj)
    def post(self):
        args = video_put_args.parse_args()
        Name=args["Name"]
        Age=args["Age"]
        Mobile=args["Mobile"]
        todo=Todo(Name=Name,Age=Age,Mobile=Mobile)
        db.session.add(todo)
        db.session.commit()
        return {"Name" :Name,"Age":Age,"Mobile":Mobile}

class EditTable(Resource):
    def put(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"Message":"Data Doesnt exist"}
        args = video_put_args.parse_args()
        Name=args['Name']
        Age=args['Age']
        Mobile=args['Mobile']
       
        todo.Name=Name
        todo.Age=Age
        todo.Mobile=Mobile
        db.session.commit()
        return{"Message":"Updated Successfully"}

    def delete(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"Message":"Data Doesnt exist"}
        db.session.delete(todo)
        db.session.commit()
        return{"Message":"Deleted Successfull"}

api.add_resource(GetTable,"/info")
api.add_resource(EditTable,"/edit/<int:sno>")

if __name__=="__main__":
    app.run(debug=True)