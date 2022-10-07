# import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if DB_USERNAME is None or DB_PASSWORD is None:
    print('DB_USERNAME or DB_PASSWORD not set')
    exit(1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/is212_g1t1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                        'pool_recycle': 280}

db = SQLAlchemy(app)
CORS(app)

# The Learning Journey Class
class LJ(db.Model):
    __tablename__ = 'Learning_Journey'
    LJ_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Staff_ID = db.Column(db.Integer, nullable=False)
    Role_ID = db.Column(db.Integer, nullable=False)
    LJ_Number = db.Column(db.Integer, nullable=False)
    def to_json(self):
        return {
            'LJ_ID': self.LJ_ID,
            'Staff_ID': self.Staff_ID,
            'Role_ID': self.Role_ID,
            'LJ_Number': self.LJ_Number
        }

class LJCourse(db.Model):
    __tablename__ = 'Learning_Journey_Course'
    LJ_ID = db.Column(db.Integer, db.ForeignKey('LJ.LJ_ID'), primary_key=True, nullable=False)
    Course_ID = db.Column(db.String(20), db.ForeignKey('course.Course_ID'), primary_key=True, nullable=False)

    def to_json(self):
        return {
            'Skill_ID': self.LJ_ID,
            'Course_ID': self.Course_ID
        }

    # this function is weird. 
    def getCoursesByLJ_ID(lj_id):
        # get role of the LJ -> find the skills related to that role -> find the courses related to that skill
        return Course.query.join(LJCourse, Course.Course_ID == LJCourse.Course_ID).where(LJCourse.LJ_ID == lj_id).all()
        

class Role(db.Model):
    __tablename__ = 'role'
    Role_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Role_Name = db.Column(db.String(50), nullable=False)
    Role_Desc = db.Column(db.String(255), nullable=False)
    Role_Is_Active = db.Column(db.Boolean, nullable=False)

    def to_json(self):
        return {
            'Role_ID': self.Role_ID,
            'Role_Name': self.Role_Name,
            'Role_Desc': self.Role_Desc,
            'Role_Is_Active': self.Role_Is_Active
        }

class Skill(db.Model):
    __tablename__ = 'skill'
    Skill_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Skill_Name = db.Column(db.String(50), nullable=False)
    Skill_Is_Active = db.Column(db.Boolean, nullable=False)

    def to_json(self):
        return {
            'Skill_ID': self.Skill_ID,
            'Skill_Name': self.Skill_Name,
            'Skill_Is_Active': self.Skill_Is_Active
        }

class Course(db.Model):
    __tablename__ = 'course'
    Course_ID = db.Column(db.String(20), primary_key=True, nullable=False)
    Course_Name = db.Column(db.String(50), nullable=False)
    Course_Desc = db.Column(db.String(255), nullable=True)
    Course_Is_Active = db.Column(db.Boolean, nullable=False)
    Course_Type = db.Column(db.String(10), nullable=True)
    Course_Category = db.Column(db.String(50), nullable=True)

    def to_json(self):
        return {
            'Course_ID': self.Course_ID,
            'Course_Name': self.Course_Name,
            'Course_Desc': self.Course_Desc,
            'Course_Is_Active': self.Course_Is_Active,
            'Course_Type': self.Course_Type,
            'Course_Category': self.Course_Category
        }

class SkillRole(db.Model):
    __tablename__ = 'skill_role'
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID'), primary_key=True, nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID'), primary_key=True, nullable=False)

    def to_json(self):
        return {
            'Skill_ID': self.Skill_ID,
            'Role_ID': self.Role_ID
        }

    def getAssignedSkillsByRoleID(role_id):
        return Skill.query.join(SkillRole, Skill.Skill_ID == SkillRole.Skill_ID).where(SkillRole.Role_ID == role_id).all()

    def getAssignedRoleBySkillID(skill_id):
        return Role.query.join(SkillRole, Role.Role_ID == SkillRole.Role_ID).where(SkillRole.Skill_ID == skill_id).all()

    def getAssignedRolesBySkillIDs(skill_ids):
        output = []
        for skill_id in skill_ids:
            skill = Skill.query.where(Skill.Skill_ID == skill_id).first()
            if(skill):
                output.append({
                    'skill': skill.to_json(),
                    'roles': [role.to_json() for role in SkillRole.getAssignedRoleBySkillID(skill_id)]
                })
        return output
    
    def getAssignedSkillByRoleID(role_id):
        return Skill.query.join(SkillRole, Skill.Skill_ID == SkillRole.Skill_ID).where(SkillRole.Role_ID == role_id).all()

class SkillCourse(db.Model):
    __tablename__ = 'course_skill'
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID'), primary_key=True, nullable=False)
    Course_ID = db.Column(db.String(20), db.ForeignKey('course.Course_ID'), primary_key=True, nullable=False)

    def to_json(self):
        return {
            'Skill_ID': self.Skill_ID,
            'Course_ID': self.Course_ID
        }

    def getAssignedCourseBySkillID(skill_id):
        return Course.query.join(SkillCourse, Course.Course_ID == SkillCourse.Course_ID).where(SkillCourse.Skill_ID == skill_id).all()

    def getAssignedCoursesBySkillIDs(skill_ids):
        output = []
        for skill_id in skill_ids:
            skill = Skill.query.where(Skill.Skill_ID == skill_id).first()
            if(skill):
                output.append({
                    'skill': skill.to_json(),
                    'courses': [course.to_json() for course in SkillCourse.getAssignedCourseBySkillID(skill_id)]
                })
        return output

    # not really needed?
    # def getAssignedSkillByCourseID(course_id):
    #     return Skill.query.join(SkillCourse, Skill.Skill_ID == SkillCourse.Skill_ID).where(SkillCourse.Course_ID == course_id).all()

# Shaan to be deleted
# @app.route('/role/role_by_skill/<int:skill_id>',methods=['GET'])
# def getRoleBySkill(skill_id):
#     try:
#         Role = SkillRole.getAssignedRoleBySkillID(skill_id)
@app.route('/LJ')
def getAllLJ():
    try:
        ljs = LJ.query.all()
        return jsonify({
            "code": 201,
            "data": [lj.to_json() for lj in ljs]
        }), 201
    except Exception: 
        return jsonify({
            "code": 500,
            "message": "Unable to get role from database"
        }), 500

# For this, I am unable to validate whether a staff has a LJ.
@app.route('/LJ/<string:Staff_ID>')
def getLJsbyStaffID(Staff_ID):
    try:
        ljs = LJ.query.filter_by(Staff_ID=Staff_ID)
        return jsonify({
            "code":201,
            "data": [lj.to_json() for lj in ljs]
        }), 201
    except Exception: 
        return jsonify({
            "code": 500,
            "message": "Unable to get LJ from database"
        })
    
@app.route('/LJ/get_courses_by_LJ_ID/<string:LJ_ID>')
def getCoursesByLJ_ID(LJ_ID):
    try: 
        courses = LJCourse.getCoursesByLJ_ID(LJ_ID)
        return jsonify({
            "code": 201,
            "data": [c.to_json() for c in courses]
        }), 201
    except Exception as e:
        print(e.args)
        return jsonify({
            "code": 500,
            "message": "Unable to get courses from database."
        }), 500

@app.route('/role')
def getAllRole():
    try:
        role = Role.query.all()
        return jsonify({
                "code": 201,
                "data": [r.to_json() for r in role]
            }), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get role from database."
        }), 500

# get role by role name
@app.route('/role/search/<string:role_name>',methods=['GET'])
def getRoleByName(role_name):
    try:
        role = Role.query.filter(Role.Role_Name.like(f'%{role_name}%')).all()
        if role:
            return jsonify({
                "code": 201,
                "data": [r.to_json() for r in role]
            }), 201
        else:
            return jsonify({
                "code": 400,
                "message": "Role not found."
            }), 400
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get role from database."
        }), 500

@app.route('/course')
def getAllCourse():
    try:
        course = Course.query.all()
        return jsonify({
                "code": 201,
                "data": [c.to_json() for c in course]
            }), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get course from database."
        }), 500

@app.route('/role/create', methods=['POST'])
def createRole():
    try:
        data = request.get_json()

        # check if data has role name
        if 'Role_Name' not in data.keys() or data['Role_Name'] == "":
            return jsonify({
                "code": 400,
                "message": "Role name cannot be empty."
            }), 400

        # role name cannot be > 50 characters
        if len(data['Role_Name']) > 50:
            return jsonify({
                "code": 400,
                "message": "Role name cannot be more than 50 characters."
            }), 400

        # check if role name already exists
        role = Role.query.filter_by(Role_Name=data['Role_Name']).first()
        if role:
            return jsonify({
                "code": 400,
                "message": "Role already exists."
            }), 400

        # default role description to empty string
        role_Desc = data['Role_Desc'] if 'Role_Desc' in data.keys() else ""

        # role desc cannot be > 255 characters
        if len(role_Desc) > 255:
            return jsonify({
                "code": 400,
                "message": "Role description cannot be more than 255 characters."
            }), 400

        if data['Role_Name'].isnumeric():
            return jsonify({
                "code": 400,
                "message": "Role name cannot be numeric."
            }), 400
        
        if role_Desc.isnumeric():
            return jsonify({
                "code": 400,
                "message": "Role description cannot be numeric."
            }), 400

        # create new role, default is active
        new_role = Role(Role_Name=data['Role_Name'], Role_Desc=role_Desc, Role_Is_Active=1)
        db.session.add(new_role)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Role created successfully.",
            "data": new_role.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to create new role. Error message: " + str(e)
        }), 500

# @app.route('/role/assigned_skills') # this one is the simulation version
# def getAssignedSkills():
#     try:
#         data = request.get_json()
#         if 'Role_ID' not in data.keys() or data['Role_ID'] == []:
#             return jsonify({
#                 "code": 400,
#                 "message": "Role ID cannot be empty."
#             }), 400
#         role_id = data['Role_ID']

#         skills = SkillRole.getAssignedSkillsByRoleID(role_id)

#         return jsonify({
#             "code": 201,
#             # "data": skills #doesn't convert by json itself, need to use .to_json() for each skill
#             "data": [s.to_json() for s in skills]
#         }), 201


#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": "Unable to get assigned skills from database. Error message: " + str(e)
#         }), 500

@app.route('/role/assigned_skills/<int:role_id>') # this one is the actual version with URL
def getAssignedSkills(role_id):
    try:
        skills = SkillRole.getAssignedSkillsByRoleID(role_id)

        return jsonify({
            "code": 201,
            # "data": skills #doesn't convert by json itself, need to use .to_json() for each skill
            "data": [s.to_json() for s in skills]
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned skills from database. Error message: " + str(e)
        }), 500

@app.route('/skill')
def getAllSkill():
    try:
        skill = Skill.query.all()
        return jsonify({
                "code": 201,
                "data": [s.to_json() for s in skill]
            }), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get skill from database."
        }), 500

@app.route('/skill/create', methods=['POST'])
def createSkill():
    try:
        data = request.get_json()

        # check if data has skill name
        if 'Skill_Name' not in data.keys() or data['Skill_Name'] == "":
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be empty."
            }), 400

        # check if length is > 50 char
        if len(data['Skill_Name']) > 50:
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be more than 50 characters."
            }), 400
        
        # check if skill name already exists
        skill = Skill.query.filter_by(Skill_Name=data['Skill_Name']).first()
        if skill:
            return jsonify({
                "code": 400,
                "message": "Skill already exists."
            }), 400

        # create new skill, default is active
        new_skill = Skill(Skill_Name=data['Skill_Name'], Skill_Is_Active=1)
        db.session.add(new_skill)
        db.session.commit() 
        return jsonify({
            "code": 201,
            "message": "Skill created successfully.",
            "data": new_skill.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to create new skill. Error message: " + str(e)
        }), 500

#activate/deactivate skill
@app.route('/skill/toggle/<int:skill_id>', methods=['PUT'])
def toggleSkill(skill_id):
    try:
        skill = Skill.query.filter_by(Skill_ID=skill_id).first()
        if not skill:
            return jsonify({
                "code": 400,
                "message": "Skill does not exist."
            }), 400

        action = "deactivated" if skill.Skill_Is_Active else "activated"
        skill.Skill_Is_Active = 0 if skill.Skill_Is_Active else 1

        db.session.commit()
        return jsonify({
            "code": 201,
            "message": f"Skill {action} successfully.",
            "data": skill.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to toggle skill. Error message: " + str(e)
        }), 500

@app.route('/skill/update', methods=['PUT'])
def updateSkill():
    try:
        data = request.get_json()
        print(data)

        # check if data has skill id?
        # check if skill id is in database?

        # check if data has skill name
        if 'Skill_Name' not in data.keys() or data['Skill_Name'] == "":
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be empty."
            }), 400

        # check if length is > 50 char
        if len(data['Skill_Name']) > 50:
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be more than 50 characters."
            }), 400

        # check if skill name already exists
        skill = Skill.query.filter_by(Skill_Name=data['Skill_Name']).first()
        if skill:
            return jsonify({
                "code": 400,
                "message": "Skill name already exists."
            }), 400

        # update skill
        skill = Skill.query.filter_by(Skill_ID=data['Skill_ID']).first()
        skill.Skill_Name = data['Skill_Name']
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Skill updated successfully.",
            "data": skill.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to update skill. Error message: " + str(e)
        }), 500

@app.route('/skill/assign_to_role', methods=['POST'])
def assignSkillToRole():
    try:
        data = request.get_json()
        print(data)
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Role_ID' not in data.keys() or not isinstance(data['Role_ID'], (int,list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Role ID cannot be empty or non interger"
            }), 400
            
        returnMessage = []
        if isinstance(data['Role_ID'],int):
            newSkillRole = SkillRole(Skill_ID=data['Skill_ID'], Role_ID=data['Role_ID'])
            db.session.add(newSkillRole)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Skill assigned to role successfully.",
                "data": newSkillRole.to_json()
            }), 201
        # assume that validation is done in the UI
        elif isinstance(data['Role_ID'],list):
            for role_id in data['Role_ID']:
                newSkillRole = SkillRole(Skill_ID=data['Skill_ID'], Role_ID=role_id)
                db.session.add(newSkillRole)
                db.session.commit()
                returnMessage.append(newSkillRole.to_json())

            return jsonify({
                "code": 201,
                "message": "Skill assigned to role successfully.",
                "data": returnMessage
            }), 201


    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to assign skill to role. Error message: " + str(e)
        }), 500

@app.route('/skill/assign_to_courses', methods=['POST'])
def assignSkillToCourses():
    try:
        data = request.get_json()
        print(data)
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Course_ID' not in data.keys() or not isinstance(data['Course_ID'], (int,list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Course ID cannot be empty or non interger"
            }), 400
            
        returnMessage = []
        if isinstance(data['Course_ID'],int):
            newSkillCourse = SkillCourse(Skill_ID=data['Skill_ID'], Course_ID=data['Course_ID'])
            db.session.add(newSkillCourse)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Skill assigned to course successfully.",
                "data": newSkillCourse.to_json()
            }), 201
        # assume that validation is done in the UI
        elif isinstance(data['Course_ID'],list):
            for course_id in data['Course_ID']:
                newSkillCourse = SkillCourse(Skill_ID=data['Skill_ID'], Course_ID=course_id)
                db.session.add(newSkillCourse)
                db.session.commit()
                returnMessage.append(newSkillCourse.to_json())

            return jsonify({
                "code": 201,
                "message": "Skill assigned to course successfully.",
                "data": returnMessage
            }), 201


    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to assign skill to course. Error message: " + str(e)
        }), 500

@app.route('/skill/assigned_courses')
def getAssignedCourses():
    try:
        data = request.get_json()
        if 'Skill_IDs' not in data.keys() or data['Skill_IDs'] == []:
            return jsonify({
                "code": 400,
                "message": "Skill ID cannot be empty."
            }), 400
        skill_ids = data['Skill_IDs']

        output = SkillCourse.getAssignedCoursesBySkillIDs(skill_ids)

        return jsonify({
            "code": 201,
            "data": output
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned course from database. Error message: " + str(e)
        }), 500

@app.route('/skill/assigned_roles')
def getAssignedRoles():
    try:
        data = request.get_json()
        if 'Skill_IDs' not in data.keys() or data['Skill_IDs'] == []:
            return jsonify({
                "code": 400,
                "message": "Skill ID cannot be empty."
            }), 400
        skill_ids = data['Skill_IDs']

        output = SkillRole.getAssignedRolesBySkillIDs(skill_ids)

        return jsonify({
            "code": 201,
            "data": output
        }), 201
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned roles from database. Error message: " + str(e)
        }), 500

@app.route('/skill/get_assigned_roles_by_ID/<int:skill_id>')
def getAssignedRoleByID(skill_id):
    try: 
        data = SkillRole.getAssignedRolesBySkillIDs([skill_id])
        return jsonify({
            "code": 201,
            "message": data
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned role from database. Error message: " + str(e)
        }), 500

@app.route('/skill/get_assigned_courses_by_ID/<int:skill_id>')
def getAssignedCoursesByID(skill_id):
    try: 
        data = SkillCourse.getAssignedCoursesBySkillIDs([skill_id])
        return jsonify({
            "code": 201,
            "message": data
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned role from database. Error message: " + str(e)
        }), 500

@app.route('/role/assigned_skill/<int:role_id>')
def getAssignedSkill(role_id):
    try:
        skills = SkillRole.getAssignedSkillByRoleID(role_id=role_id)
        return jsonify({
                "code": 201,
                "data": [s.to_json() for s in skills]
            }), 201
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to get assigned skill from database. Error message: " + str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=456, debug=True)
