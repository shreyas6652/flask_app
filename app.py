from flask import Flask,jsonify
from flask_restful import Api,Resource,fields, marshal_with,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
app=Flask(__name__)
api=Api(app)
CORS(app,resources=r'/api/*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'https://murmuring-coast-63289.herokuapp.com/postgres://yrptuivhfcysqz:1835b36ef415f55e524653e03430d729090b4fb9a83e6e968532f1dcd496d6f4@ec2-52-203-74-38.compute-1.amazonaws.com:5432/d73a2mgafbngcf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=True)
    Age = db.Column(db.String(500), nullable=True)
    Mobile = db.Column(db.String(500), nullable=True)
#classModel->serial->View(Crud)
resource_fields={
    'sno':fields.Integer,
    'Name':fields.String,
    'Age':fields.Integer,
    'Mobile':fields.String
}

info_put_args = reqparse.RequestParser()
info_put_args.add_argument("Name", type=str, required=True)
info_put_args.add_argument("Age", type=str, required=True)
info_put_args.add_argument("Mobile", type=str,  required=True)

class GetTable(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result=Todo.query.all()
        print(type(result))
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
        args = info_put_args.parse_args()
        Name=args["Name"]
        Age=args["Age"]
        Mobile=args["Mobile"]
        todo=Todo(Name=Name,Age=Age,Mobile=Mobile)
        db.session.add(todo)
        db.session.commit()
        return {"Name" :Name,"Age":Age,"Mobile":Mobile}

class EditTable(Resource):
    def get(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        
        return {"Name":todo.Name,"Age":todo.Age,"Mobile":todo.Mobile}
    def put(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"Message":"Data Doesnt exist"}
        args = info_put_args.parse_args()
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

api.add_resource(GetTable,"/api/info")
api.add_resource(EditTable,"/api/edit/<int:sno>")

if __name__=="__main__":
    app.run(debug=True)