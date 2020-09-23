from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import os

# https://stackoverflow.com/questions/18208492/sqlalchemy-exc-operationalerror-operationalerror-unable-to-open-database-file/44687471
file_path = os.path.abspath(os.getcwd())+"\chinook.db"

# SQLite
# CONNECTION_STRING = 'sqlite:////chinook.db'
# db_connect = create_engine(CONNECTION_STRING)
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db_connect = create_engine('sqlite:///'+file_path)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from employees")
        return {'employees': [i[0] for i in query.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        last_name = request.json['LastName']
        first_name = request.json['FirstName']
        title = request.json['Title']
        reports_to = request.json['ReportsTo']
        birth_date = request.json['BirthDate']
        hire_date = request.json['HireDate']
        address = request.json['Address']
        city = request.json['City']
        state = request.json['State']
        country = request.json['Country']
        postal_code = request.json['PostalCode']
        phone = request.json['Phone']
        fax = request.json['Fax']
        email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(last_name, first_name, title,
                                             reports_to, birth_date, hire_date, address,
                                             city, state, country, postal_code, phone, fax,
                                             email))
        return {'status': 'Nuevo empleado añadido'}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class EmployeeData(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(EmployeeData, '/employees/<employee_id>')  # Route_3

if __name__ == '__main__':
    app.run(port='5000')
