import json


from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


@app.route('/role')
def get_role():
    try:
        return jsonify({
            "code": 201,
            "data": [
                {'Role_ID': 1,
                 'Role_Name': "SWE",
                 'Role_Desc': "Software Engineer",
                 'Role_Is_Active': 1},
                {'Role_ID': 2,
                 'Role_Name': "PM",
                 'Role_Desc': "Project Manager",
                 'Role_Is_Active': 1}
            ]
        }
        ), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get role from database."
        }), 500


@app.route('/role/create', methods=['POST'])
def create_role():
    try:
        data = request.get_json()
        print(data)
        # role description and is active should be optional
        if(data['Role_ID'] and data['Role_Name'] and data['Role_Desc'] and data['Role_Is_Active']):  
            return jsonify({
                "code": 201,
                "message": "Role created successfully."
            }), 201
        else:
            raise Exception
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable create new role."
        }), 500


@app.route('/skill')
def get_skill():
    try:
        return jsonify({
            "code": 201,
            "data": [
                {'Skill_ID':1, 'Skill_Name':"Basic programming 1", 'Skill_Is_Active':1},
                {'Skill_ID':2, 'Skill_Name':"Basic programming 2", 'Skill_Is_Active':1},
                {'Skill_ID':3, 'Skill_Name':"Intermediate programming 1", 'Skill_Is_Active':1}
            ]
        }
        ), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get skill from database."
        }), 500


@app.route('/skill/create', methods=['POST'])
def create_skill():
    try:
        data = request.get_json()
        print(data)
        # skill is active should be optional
        if(data['Skill_ID'] and data['Skill_Name'] and data['Skill_Is_Active']):
            return jsonify({
                "code": 201,
                "message": "Skill created successfully."
            }), 201
        else:
            raise Exception
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to create skill."
        }), 500


@app.route('/skill/update', methods=['PUT'])
def update_skill():
    try:
        data = request.get_json()
        print(data)
        # skill is active should be optional
        if(data['Skill_ID'] and data['Skill_Name'] and data['Skill_Is_Active']):
            return jsonify({
                "code": 201,
                "message": "Skill updated successfully."
            }), 201
        else:
            raise Exception
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to update skill."
        }), 500


@app.route('/skill/assign_to_role', methods=['POST'])
def assign_skill_to_role():
    try:
        data = request.get_json()
        if(data['Skill_ID'] and data['Role_ID']):
            return jsonify({
                "code": 201,
                "message": "Skill assigned to role successfully."
            }), 201
        else:
            raise Exception
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to assign skill to role."
        }), 500

@app.route('/skill/assign_to_course', methods=['POST'])
def assign_skill_to_course():
    try:
        data = request.get_json()
        if(data['Skill_ID'] and data['Course_ID']):
            return jsonify({
                "code": 201,
                "message": "Skill assigned to course successfully."
            }), 201
        else:
            raise Exception
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to assign skill to course."
        }), 500

# TODO: will probably change this, im not sure how useful this is
@app.route('/skill/assigned_course/<int:skill_id>')
def get_assigned_course(skill_id):
    try:
        return jsonify({
            "code": 201,
            "data": [
                {'Skill_ID': skill_id, 'Course_ID': 1},
                {'Skill_ID': skill_id, 'Course_ID': 2},
                {'Skill_ID': skill_id, 'Course_ID': 3}
            ]
        }
        ), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned course from database."
        }), 500
        
# TODO: will probably change this, im not sure how useful this is
@app.route('/skill/assigned_role/<int:skill_id>')
def get_assigned_role(skill_id):
    try:
        return jsonify({
            "code": 201,
            "data": [
                {'Skill_ID': skill_id, 'Role_ID': 1},
                {'Skill_ID': skill_id, 'Role_ID': 2},
                {'Skill_ID': skill_id, 'Role_ID': 3}
            ]
        }
        ), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned role from database."
        }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=456, debug=True)
