# import json
from calendar import c
from time import sleep
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


class Staff(db.Model):
    __tablename__ = 'staff'
    Staff_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Position_ID = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'staff_ID': self.Staff_ID,
            'staff_FName': self.Staff_FName,
            'staff_LName': self.Staff_LName,
            'dept': self.Dept,
            'email': self.Email,
            'position_ID': self.Position_ID
        }

    def get_login_info(self):
        return {
            'staff_ID': self.Staff_ID,
            'email': self.Email,
            'position_ID': self.Position_ID,
            'staff_FName': self.Staff_FName,
        }

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
    Skill_ID = db.Column(db.Integer, db.ForeignKey(
        'skill.Skill_ID'), primary_key=True, nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey(
        'role.Role_ID'), primary_key=True, nullable=False)

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
    Skill_ID = db.Column(db.Integer, db.ForeignKey(
        'skill.Skill_ID'), primary_key=True, nullable=False)
    Course_ID = db.Column(db.String(20), db.ForeignKey(
        'course.Course_ID'), primary_key=True, nullable=False)

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


class LJSkillCourse(db.Model):
    __tablename__ = 'Learning_Journey_Course'
    LJ_ID = db.Column(db.Integer, db.ForeignKey(LJ.LJ_ID),
                      primary_key=True, nullable=False)
    Course_ID = db.Column(db.String(20), db.ForeignKey(
        Course.Course_ID), primary_key=True, nullable=False)
    Skill_ID = db.Column(db.String(20), db.ForeignKey(
        Skill.Skill_ID), primary_key=False, nullable=False)

    def to_json(self):
        return {
            'LJ_ID': self.LJ_ID,
            'Course_ID': self.Course_ID,
            'Skill_ID': self.Skill_ID
        }

    # this function is weird.
    def getCoursesByLJ_ID(lj_id):
        # get role of the LJ -> find the skills related to that role -> find the courses related to that skill
        return Course.query.join(LJSkillCourse, Course.Course_ID == LJSkillCourse.Course_ID).where(LJSkillCourse.LJ_ID == lj_id).all()

    def getCourseSkillByLJ_ID(lj_id):
        # Error Here
        return db.session.query(LJSkillCourse, Skill, Course).filter(
            LJSkillCourse.LJ_ID == lj_id
        ) .filter(
            LJSkillCourse.Skill_ID == Skill.Skill_ID
        ) .filter(
            LJSkillCourse.Course_ID == Course.Course_ID
        ).all()


@app.route('/staff')
def get_staff():
    staff = Staff.query.all()
    # return jsonify([s.to_json() for s in staff])
    return jsonify([s.get_login_info() for s in staff])


@app.route('/staff/<int:staff_ID>')
def get_staff_by_id(staff_ID):
    staff = Staff.query.filter_by(Staff_ID=staff_ID).first()
    return jsonify(staff.to_json())


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
        roles = Role.query.all()
        return jsonify({
            "code": 201,
            "data": [lj.to_json() for lj in ljs],
            "role_data": [role.to_json() for role in roles]
        }), 201
    except Exception:
        return jsonify({
            "code": 500,
            "message": "Unable to get LJ from database"
        })


@app.route('/LJ/get_courses_by_LJ_ID/<string:LJ_ID>')
def getCoursesByLJ_ID(LJ_ID):
    try:
        courses = LJSkillCourse.getCoursesByLJ_ID(LJ_ID)
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


@app.route('/LJ/addLJ', methods=["POST"])
def createLJ():
    try:
        data = request.get_json()
        keys = set(data.keys())
        check = set(["Role_ID", "Staff_ID", "LJ_Number",
                    "LJ_Courses", "LJ_Skills"])

        # check if the keys are correct
        if keys != check:
            return jsonify({
                "code": 400,
                "message": 'Fields must match "Role_ID","Staff_ID","LJ_Number","LJ_Courses" .'
            }), 400
        # check if the data are all inputted
        if "" in data.values():
            return jsonify({
                "code": 400,
                "message": 'Fields cannot be empty'
            }), 400

        # check if this user already has an LJ with the same role
        lj = LJ.query.filter_by(
            Role_ID=data['Role_ID'], Staff_ID=data['Staff_ID']).first()
        if lj:
            return jsonify({
                "code": 400,
                "message": "LJ already exists."
            }), 400

        # add to LJ table (who owns the learning journey)
        new_LJ = LJ(
            Staff_ID=data['Staff_ID'], Role_ID=data["Role_ID"], LJ_Number=data["LJ_Number"])
        db.session.add(new_LJ)
        db.session.commit()
        print(new_LJ.LJ_ID)
        # add LJ to the LJSkillCourse table
        for i in range(len(data['LJ_Skills'])):
            new_LJSkillCourse = LJSkillCourse(
                LJ_ID=new_LJ.LJ_ID, Course_ID=data['LJ_Courses'][i], Skill_ID=data['LJ_Skills'][i])
            db.session.add(new_LJSkillCourse)
        db.session.commit()

        # add courses tagged to newly created learning journey ID
        # new_LJ_Course = LJSkillCourse(LJ_ID=new_LJ.LJ_ID, Course_ID=data["LJ_Courses"])
        # db.session.add(new_LJ_Course)
        # db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Role created successfully.",
            "data": new_LJ.to_json()
        }), 201

    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "message": "Unable to create new LJ. Error message: " + str(e)
        }), 500

@app.route('/LJ/addLJ/Course', methods=["POST"])
def addCourseToLJ():
    try:
        data = request.get_json()
        keys = set(data.keys())
        check = set(["LJ_ID", "Course_ID", "Skill_ID"])

        # check staff id? 

        # check if the keys are correct
        if keys != check:
            return jsonify({
                "code": 400,
                "message": 'Fields must match "LJ_ID","Course_ID","Skill_ID"'
            }), 400
        # check if the data are all inputted
        if "" in data.values():
            return jsonify({
                "code": 400,
                "message": 'Fields cannot be empty'
            }), 400

        # check if this user already has an LJ with the same role
        lj = LJSkillCourse.query.filter_by(LJ_ID=data['LJ_ID'], Course_ID=data['Course_ID'], Skill_ID=data['Skill_ID']).first()
        if lj:
            return jsonify({
                "code": 400,
                "message": "Course already exists in the LJ."
            }), 400

        # check if skill is mapped to course
        skillCourseMap = SkillCourse.query.filter_by(Course_ID=data['Course_ID'], Skill_ID=data['Skill_ID']).first()
        if not skillCourseMap:
            return jsonify({
                "code": 400,
                "message": "Skill is not mapped to course."
            }), 400

        #check if skill is mapped to role
        roleID = LJ.query.filter_by(LJ_ID=data['LJ_ID']).first().Role_ID
        skillRoleMap = SkillRole.query.filter_by(Role_ID=roleID, Skill_ID=data['Skill_ID']).first()
        if not skillRoleMap:
            return jsonify({
                "code": 400,
                "message": "Skill is not mapped to role."
            }), 400

        # add to LJSkillCourse
        new_LJ = LJSkillCourse(
            LJ_ID=data['LJ_ID'], Course_ID=data["Course_ID"], Skill_ID=data["Skill_ID"])
        db.session.add(new_LJ)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Course added successfully.",
            "data": new_LJ.to_json()
        }), 201

    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "message": "Unable to create new LJ. Error message: " + str(e)
        }), 500


@app.route('/LJ/getCourseAndSkillByLJ_ID/<string:LJ_ID>', methods=["GET"])
def getCourseAndSkillByLJ_ID(LJ_ID):
    try:
        skill_course = LJSkillCourse.getCourseSkillByLJ_ID(LJ_ID)
        print(skill_course)
        data = []
        entries = []
        for tple in skill_course:
            entries = {}
            counter = 0
            for idx, entry in enumerate(tple):
                counter += 1
                if counter == 2:

                    entries['Skill_ID'] = entry.to_json().get('Skill_ID')
                    entries['Skill_Name'] = entry.to_json().get('Skill_Name')
                if counter == 3:
                    entries['Course_ID'] = entry.to_json().get('Course_ID')
                    entries['Course_Name'] = entry.to_json().get('Course_Name')
            data.append(entries)
        print(data)
        return jsonify({
            "code": 201,
            "data": data
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "message": "Unable to create new LJ. Error message: " + str(e)
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

# not in use
@app.route('/role/search/<string:role_name>', methods=['GET'])
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
        print(data.keys())
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
        new_role = Role(Role_Name=data['Role_Name'],
                        Role_Desc=role_Desc, Role_Is_Active=1)
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


@app.route('/role/update', methods=['PUT'])
def updateRole():
    """
    expected json imput:
    {
        "Role_ID": 1,
        "Role_Name": "SWE",
        "Role_Desc": "Software Engineer"
    }
    """
    try:
        data = request.get_json()

        # check if data has role id
        if 'Role_ID' not in data.keys():
            return jsonify({
                "code": 400,
                "message": "Role ID cannot be empty."
            }), 400

        # check if role id is int
        if not isinstance(data['Role_ID'], int):
            return jsonify({
                "code": 400,
                "message": "Role ID must be an integer."
            }), 400

        # check if role id exists
        role = Role.query.filter_by(Role_ID=data['Role_ID']).first()
        if not role:
            return jsonify({
                "code": 400,
                "message": "Role ID not found."
            }), 400

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

        # check if role is active
        # role = Role.query.filter_by(Role_ID=data['Role_ID']).first()
        # if not role.Role_Is_Active:
        #     return jsonify({
        #         "code": 400,
        #         "message": "Role is deactivated."
        #     }), 400

        # update role
        role = Role.query.filter_by(Role_ID=data['Role_ID']).first()
        role.Role_Name = data['Role_Name']
        role.Role_Desc = role_Desc
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Role updated successfully.",
            "data": role.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to update role. Error message: " + str(e)
        }), 500

@app.route('/role/<string:role_id>', methods=['GET'])
def getRole(role_id):
    try:
        role = Role.query.filter_by(Role_ID=role_id).first()
        if role:
            return jsonify({
                "code": 201,
                "data": role.to_json()
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

# this one is the actual version with URL
@app.route('/role/assigned_skills/<int:role_id>')
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

# activate/deactivate role


@app.route('/role/toggle/<int:role_id>', methods=['PUT'])
def toggleRole(role_id):
    try:
        role = Role.query.filter_by(Role_ID=role_id).first()
        if not role:
            return jsonify({
                "code": 400,
                "message": "Role does not exist."
            }), 400

        action = "deactivated" if role.Role_Is_Active else "activated"
        role.Role_Is_Active = 0 if role.Role_Is_Active else 1

        db.session.commit()
        return jsonify({
            "code": 201,
            "message": f"Role {action} successfully.",
            "data": role.to_json()
        }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to toggle role. Error message: " + str(e)
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

        # check if skill name is numeric
        if data['Skill_Name'].isnumeric():
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be numeric."
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

# activate/deactivate skill


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

        # check if data has skill id
        if 'Skill_ID' not in data.keys():
            return jsonify({
                "code": 400,
                "message": "Skill ID cannot be empty."
            }), 400

        # check if skill id is int
        if not isinstance(data['Skill_ID'], int):
            return jsonify({
                "code": 400,
                "message": "Skill ID must be an integer."
            }), 400

        # check if skill id exists
        skill = Skill.query.filter_by(Skill_ID=data['Skill_ID']).first()
        if not skill:
            return jsonify({
                "code": 400,
                "message": "Skill does not exist."
            }), 400

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

        # check if skill name is numeric
        if data['Skill_Name'].isnumeric():
            return jsonify({
                "code": 400,
                "message": "Skill name cannot be numeric."
            }), 400

        # check if skill is active
        # skill = Skill.query.filter_by(Skill_ID=data['Skill_ID']).first()
        # if not skill.Skill_Is_Active:
        #     return jsonify({
        #         "code": 400,
        #         "message": "Skill is deactivated."
        #     }), 400

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
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Role_ID' not in data.keys() or not isinstance(data['Role_ID'], (int, list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Role ID cannot be empty or non interger"
            }), 400

        if isinstance(data['Role_ID'], list) and len(data['Role_ID']) == 0:
            return jsonify({
                "code": 400,
                "message": "Role ID cannot be empty list"
            }), 400

        returnMessage = []
        if isinstance(data['Role_ID'], int):
            newSkillRole = SkillRole(
                Skill_ID=data['Skill_ID'], Role_ID=data['Role_ID'])
            db.session.add(newSkillRole)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Role(s) assigned to Skill successfully.",
                "data": newSkillRole.to_json()
            }), 201
        # assume that validation is done in the UI
        elif isinstance(data['Role_ID'], list):
            for role_id in data['Role_ID']:
                newSkillRole = SkillRole(
                    Skill_ID=data['Skill_ID'], Role_ID=role_id)
                db.session.add(newSkillRole)
                db.session.commit()
                returnMessage.append(newSkillRole.to_json())

            return jsonify({
                "code": 201,
                "message": "Role(s) assigned to Skill successfully.",
                "data": returnMessage
            }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to assign skill to role. Error message: " + str(e)
        }), 500


@app.route('/skill/unassign_role_from_skill', methods=['DELETE'])
def unassignRoleFromSkill():
    try:
        data = request.get_json()
        print(data)
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Role_ID' not in data.keys() or not isinstance(data['Role_ID'], (int, list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Role ID cannot be empty or non interger"
            }), 400

        if isinstance(data['Role_ID'], list) and len(data['Role_ID']) == 0:
            return jsonify({
                "code": 400,
                "message": "Role ID cannot be empty list"
            }), 400

        if isinstance(data['Role_ID'], int):
            skillRole = SkillRole.query.filter_by(
                Skill_ID=data['Skill_ID'], Role_ID=data['Role_ID']).first()
            if not skillRole:
                return jsonify({
                    "code": 400,
                    "message": "Skill and role does not exist."
                }), 400
            db.session.delete(skillRole)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Role unassigned from skill successfully.",
                "data": skillRole.to_json()
            }), 201
        elif isinstance(data['Role_ID'], list):
            returnMessage = []
            for role_id in data['Role_ID']:
                skillRole = SkillRole.query.filter_by(
                    Skill_ID=data['Skill_ID'], Role_ID=role_id).first()
                if not skillRole:
                    return jsonify({
                        "code": 400,
                        "message": "Skill and role does not exist."
                    }), 400
                db.session.delete(skillRole)
                db.session.commit()
                returnMessage.append(skillRole.to_json())
            return jsonify({
                "code": 201,
                "message": "Role unassigned from skill successfully.",
                "data": returnMessage
            }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to unassign role from skill. Error message: " + str(e)
        }), 500


@app.route('/skill/assign_to_courses', methods=['POST'])
def assignSkillToCourses():
    try:
        data = request.get_json()
        print(data)
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Course_ID' not in data.keys() or not isinstance(data['Course_ID'], (str, list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Course ID must be an integer and string respectively"
            }), 400

        if isinstance(data['Course_ID'], list) and len(data['Course_ID']) == 0:
            return jsonify({
                "code": 400,
                "message": "Course ID cannot be empty list"
            }), 400


        returnMessage = []
        if isinstance(data['Course_ID'], str):
            newSkillCourse = SkillCourse(
                Skill_ID=data['Skill_ID'], Course_ID=data['Course_ID'])
            db.session.add(newSkillCourse)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Course assigned to course successfully.",
                "data": newSkillCourse.to_json()
            }), 201
        # assume that validation is done in the UI
        elif isinstance(data['Course_ID'], list):
            for course_id in data['Course_ID']:
                newSkillCourse = SkillCourse(
                    Skill_ID=data['Skill_ID'], Course_ID=course_id)
                db.session.add(newSkillCourse)
                db.session.commit()
                returnMessage.append(newSkillCourse.to_json())

            return jsonify({
                "code": 201,
                "message": "Course(s) assigned to skill successfully.",
                "data": returnMessage
            }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to assign course to skill. Error message: " + str(e)
        }), 500


@app.route('/skill/unassign_course_from_skill', methods=['DELETE'])
def unassignCourseFromSkill():
    try:
        data = request.get_json()
        print(data)
        if 'Skill_ID' not in data.keys() or not isinstance(data['Skill_ID'], int) or 'Course_ID' not in data.keys() or not isinstance(data['Course_ID'], (str, list)):
            return jsonify({
                "code": 400,
                "message": "Skill ID and Course ID must be an integer and string respectively"
            }), 400

        if isinstance(data['Course_ID'], list) and len(data['Course_ID']) == 0:
            return jsonify({
                "code": 400,
                "message": "Course ID cannot be empty list"
            }), 400

        if isinstance(data['Course_ID'], str):
            skillCourse = SkillCourse.query.filter_by(
                Skill_ID=data['Skill_ID'], Course_ID=data['Course_ID']).first()
            if not skillCourse:
                return jsonify({
                    "code": 400,
                    "message": "Skill and course does not exist."
                }), 400
            db.session.delete(skillCourse)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Course unassigned from skill successfully.",
                "data": skillCourse.to_json()
            }), 201
        elif isinstance(data['Course_ID'], list):
            returnMessage = []
            for course_id in data['Course_ID']:
                skillCourse = SkillCourse.query.filter_by(
                    Skill_ID=data['Skill_ID'], Course_ID=course_id).first()
                if not skillCourse:
                    return jsonify({
                        "code": 400,
                        "message": "Skill and course does not exist."
                    }), 400
                db.session.delete(skillCourse)
                db.session.commit()
                returnMessage.append(skillCourse.to_json())
            return jsonify({
                "code": 201,
                "message": "Course unassigned from skill successfully.",
                "data": returnMessage
            }), 201

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Unable to unassign course from skill. Error message: " + str(e)
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
            "message": "Unable to get assigned courses from database. Error message: " + str(e)
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

# duplicated code, to remove after testing front end
# @app.route('/role/assigned_skill/<int:role_id>')
# def getAssignedSkill(role_id):
#     try:
#         skills = SkillRole.getAssignedSkillByRoleID(role_id=role_id)
#         return jsonify({
#             "code": 201,
#             "data": [s.to_json() for s in skills]
#         }), 201
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": "Unable to get assigned skill from database. Error message: " + str(e)
#         }), 500


@app.route('/LJ/deleteLJ/<int:lj_id>')
def deleteLJ(lj_id):
    try:
        data = LJ.query.filter_by(LJ_ID=lj_id).first()
        if not data:
            return jsonify({
                "code": 400,
                "message": "Learning Journey does not exist."
            }), 400

        if data:
            db.session.delete(data)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Learning Journey deleted successfully."
            }), 201
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": "Unable to delete LJ from database. Error message: " + str(e)
        }), 400

@app.route('/course/delete/<string:course_id>/<int:lj_id>')
def deleteCourse(course_id, lj_id):
    try:
        course = LJSkillCourse.query.filter_by(LJ_ID=lj_id, Course_ID=course_id).first()
        if not course:
            return jsonify({
                "code": 400,
                "message": "Cannot delete course. Learning Journey with Course selected does not exist."
            }), 400

        course_count = LJSkillCourse.query.filter_by(LJ_ID=lj_id).count()
        if course_count == 1:
            return jsonify({
                "code": 400,
                "message": "Cannot delete course. At least one course is required."
            }), 400

        if course:
            db.session.delete(course)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Course deleted successfully."
            }), 201
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": "Unable to delete course from database. Error message: " + str(e)
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=456, debug=True)
