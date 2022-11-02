import unittest
import flask_testing
import json
# from sqlalchemy import event

from flaskServer import *

class TestApp(flask_testing.TestCase):

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
   
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    # https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys
    # Ensure FOREIGN KEY for sqlite3
    # not working
    # event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        db.session.add_all([
            Course(Course_ID="IS-1", Course_Name="Information Systems & Innovation", Course_Desc="case aborum.", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-2", Course_Name="Business Process Analysis and Solutioning", Course_Desc="modeling, lorem ipsum doloraborum.", Course_Is_Active=1, Course_Type="External", Course_Category="Technical"),
            Course(Course_ID="IS-3", Course_Name="Enterprise Solution Management", Course_Desc="incident management, problem management, change management, borum.", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-4", Course_Name="Software Project Management", Course_Desc="agile, scrum, waterfall", Course_Is_Active=0, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-5", Course_Name="Digital Business - Technology and Transformation", Course_Desc="emerging technologies", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-6", Course_Name="Introduction to Programming", Course_Desc="basic python", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-7", Course_Name="Data Management", Course_Desc="mySQL, ERD", Course_Is_Active=0, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-8", Course_Name="Interaction Design and Prototyping", Course_Desc="Prototyping, product management", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-9", Course_Name="Web Application Development I", Course_Desc="php, html", Course_Is_Active=1, Course_Type="Internal", Course_Category="Technical"),
            Course(Course_ID="IS-10", Course_Name="Web Application Development II", Course_Desc="css, javascript, bootstrap, vue.js", Course_Is_Active=1, Course_Type="External", Course_Category="HR"),
            Course(Course_ID="IS-11", Course_Name="Enterprise Solution Development", Course_Desc="Microserivces, API, REST", Course_Is_Active=1, Course_Type="Internal", Course_Category="Finance"),

            Skill(Skill_ID=1, Skill_Name="Basic programming 1", Skill_Is_Active=1),
            Skill(Skill_ID=2, Skill_Name="Basic programming 2", Skill_Is_Active=1),
            Skill(Skill_ID=3, Skill_Name="Intermediate programming 1", Skill_Is_Active=1),
            Skill(Skill_ID=4, Skill_Name="Intermediate programming 2", Skill_Is_Active=1),
            Skill(Skill_ID=5, Skill_Name="Modeling 1", Skill_Is_Active=1),
            Skill(Skill_ID=6, Skill_Name="Agile 1", Skill_Is_Active=1),
            Skill(Skill_ID=7, Skill_Name="Critical thinking 1", Skill_Is_Active=1),
            Skill(Skill_ID=8, Skill_Name="Database 1", Skill_Is_Active=1),
            Skill(Skill_ID=9, Skill_Name="Front end 1", Skill_Is_Active=1),
            Skill(Skill_ID=10, Skill_Name="Business process management 1", Skill_Is_Active=1),
            Skill(Skill_ID=11, Skill_Name="Prototyping 1", Skill_Is_Active=0),

            Staff(Staff_ID=1, Staff_FName="John", Staff_LName="Smith", Dept="IT", Email="john.smith@gmail.com", Position_ID=1),
            Staff(Staff_ID=2, Staff_FName="Jane", Staff_LName="Doe", Dept="IT", Email="jane.doe@gmail.com", Position_ID=1),
            Staff(Staff_ID=3, Staff_FName="Maria", Staff_LName="Lee", Dept="HR", Email="maria.lee@gmail.com", Position_ID=1),
            Staff(Staff_ID=4, Staff_FName="David", Staff_LName="Lai", Dept="Production", Email="david.lai@gmail.com", Position_ID=2),
            Staff(Staff_ID=5, Staff_FName="Ana", Staff_LName="Yee", Dept="Operations", Email="ana.yee@gmail.com", Position_ID=2),
            Staff(Staff_ID=6, Staff_FName="Michael", Staff_LName="Teo", Dept="Operations", Email="michael.teo@gmail.com", Position_ID=2),
            Staff(Staff_ID=7, Staff_FName="Carlos", Staff_LName="Tan", Dept="Services", Email="carlos.tan@gmail.com", Position_ID=3),
            Staff(Staff_ID=8, Staff_FName="James", Staff_LName="Yang", Dept="Customer Relations", Email="james.yang@gmail.com", Position_ID=3),
            Staff(Staff_ID=9, Staff_FName="Sandra", Staff_LName="Chua", Dept="HR", Email="sandra.chua@gmail.com", Position_ID=3),
            Staff(Staff_ID=10, Staff_FName="Sarah", Staff_LName="Lim", Dept="Accounting", Email="sarah.lim@gmail.com", Position_ID=2),
            Staff(Staff_ID=11, Staff_FName="Mark", Staff_LName="Chen", Dept="Accounting", Email="mark.chen@gmail.com", Position_ID=1),

            Role(Role_ID=1, Role_Name="SWE", Role_Desc= "Software Engineer", Role_Is_Active= 1),
            Role(Role_ID=2, Role_Name="PM", Role_Desc= "Project Manager", Role_Is_Active= 1),
            Role(Role_ID=3, Role_Name="BA", Role_Desc= "Business Analyst", Role_Is_Active= 0),

            # Registration(Reg_ID=12345, Course_ID="IS-1", Staff_ID=4, Reg_Status="Registered", Completion_Status="Completed"),
            # Registration(Reg_ID=12346, Course_ID="IS-1", Staff_ID=5, Reg_Status="Registered", Completion_Status="Completed")),

            SkillCourse(Course_ID="IS-1", Skill_ID=1),
            SkillCourse(Course_ID="IS-1", Skill_ID=2),

            SkillRole(Skill_ID=1, Role_ID=1),
            SkillRole(Skill_ID=2, Role_ID=2),
            SkillRole(Skill_ID=2, Role_ID=1),

            LJ(LJ_ID=1, Staff_ID=1, Role_ID=1, LJ_Number=1),
            LJ(LJ_ID=2, Staff_ID=1, Role_ID=2, LJ_Number=2),
            LJ(LJ_ID=3, Staff_ID=1, Role_ID=3, LJ_Number=3),
            LJ(LJ_ID=4, Staff_ID=4, Role_ID=1, LJ_Number=1),
            LJ(LJ_ID=5, Staff_ID=4, Role_ID=2, LJ_Number=2),
            LJ(LJ_ID=6, Staff_ID=4, Role_ID=3, LJ_Number=3),

            LJSkillCourse(LJ_ID=1, Course_ID="IS-1", Skill_ID=1),
            LJSkillCourse(LJ_ID=1, Course_ID="IS-2", Skill_ID=2),
            LJSkillCourse(LJ_ID=2, Course_ID="IS-3", Skill_ID=3),
            LJSkillCourse(LJ_ID=2, Course_ID="IS-4", Skill_ID=4),
            LJSkillCourse(LJ_ID=3, Course_ID="IS-5", Skill_ID=5),
            LJSkillCourse(LJ_ID=3, Course_ID="IS-6", Skill_ID=6),
            LJSkillCourse(LJ_ID=4, Course_ID="IS-1", Skill_ID=1),
            LJSkillCourse(LJ_ID=4, Course_ID="IS-2", Skill_ID=2),
            LJSkillCourse(LJ_ID=5, Course_ID="IS-3", Skill_ID=3),
            LJSkillCourse(LJ_ID=5, Course_ID="IS-4", Skill_ID=4),
            LJSkillCourse(LJ_ID=6, Course_ID="IS-5", Skill_ID=5),

        ])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestSkillR(TestApp):
    # read methods
    def test_getSkills(self):
        response = self.client.get('/skill')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']

        self.assertEqual(data[0], {'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 1'})
        self.assertEqual(data, [{'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 1'}, {'Skill_ID': 2, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 2'}, {'Skill_ID': 3, 'Skill_Is_Active': True, 'Skill_Name': 'Intermediate programming 1'}, {'Skill_ID': 4, 'Skill_Is_Active': True, 'Skill_Name': 'Intermediate programming 2'}, {'Skill_ID': 5, 'Skill_Is_Active': True, 'Skill_Name': 'Modeling 1'}, {'Skill_ID': 6, 'Skill_Is_Active': True, 'Skill_Name': 'Agile 1'}, {'Skill_ID': 7, 'Skill_Is_Active': True, 'Skill_Name': 'Critical thinking 1'}, {'Skill_ID': 8, 'Skill_Is_Active': True, 'Skill_Name': 'Database 1'}, {'Skill_ID': 9, 'Skill_Is_Active': True, 'Skill_Name': 'Front end 1'}, {'Skill_ID': 10, 'Skill_Is_Active': True, 'Skill_Name': 'Business process management 1'}, {'Skill_ID': 11, 'Skill_Is_Active': False, 'Skill_Name': 'Prototyping 1'}])

class TestSkillC(TestApp):
    # create methods
    def test_createSkill(self):
        response = self.client.post('/skill/create', json={'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Skill_ID': 12, 'Skill_Is_Active': True, 'Skill_Name': 'testSkill'})

    def test_createSkillEmptyName(self):
        response = self.client.post('/skill/create', json={'Skill_Name': ''})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be empty.")

        response = self.client.post('/skill/create', json={})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be empty.")

    def test_createSkillBoundary50Chars(self):
        response = self.client.post('/skill/create', json={'Skill_Name': 't' * 50})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Skill_ID': 12, 'Skill_Is_Active': True, 'Skill_Name': 't' * 50})

        response = self.client.post('/skill/create', json={'Skill_Name': 't' * 51})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be more than 50 characters.")

    def test_createSkillAlreadyExists(self):
        response = self.client.post('/skill/create', json={'Skill_Name': 'Basic programming 1'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill already exists.")

    def test_createSkillNameNumeric(self):
        response = self.client.post('/skill/create', json={'Skill_Name': '123'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be numeric.")

class TestSkillU(TestApp):
    # update methods
    def test_updateSkill(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        message = json.loads(response.data)['message']
        self.assertEqual(data, {'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'testSkill'})
        self.assertEqual(message, "Skill updated successfully.")

    # should never happen given the front end
    def test_updateSkillEmptyID(self):
        response = self.client.put('/skill/update', json={'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID cannot be empty.")

    # should never happen given the front end
    def test_updateSkillIDNotFound(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 100, 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill does not exist.")

    # should never happen given the front end
    def test_updateSkillIDNotInterger(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 'abc', 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID must be an integer.")

        response = self.client.put('/skill/update', json={'Skill_ID': '', 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID must be an integer.")

    def test_updateSkillEmptyName(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': ''})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be empty.")

        response = self.client.put('/skill/update', json={'Skill_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be empty.")

    def test_updateSkillAlreadyExists(self):
        response = self.client.put('/skill/update', json={"Skill_ID": 1, 'Skill_Name': 'Basic programming 2'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name already exists.")

    def test_updateSkillBoundary50Chars(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': 't' * 50})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 't' * 50})

        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': 't' * 51})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be more than 50 characters.")

    def test_updateSkillNameNumeric(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': '123'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name cannot be numeric.")

class TestSkillD(TestApp):
    # delete methods
    def test_deactivateSkill(self):
        response = self.client.put('/skill/toggle/1')
        self.assertEqual(response.status_code, 201)

        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(message, "Skill deactivated successfully.")
        self.assertEqual(data, {
            "Skill_ID": 1,
            "Skill_Is_Active": False,
            "Skill_Name": "Basic programming 1"
        })

        response = self.client.put('/skill/toggle/1')
        self.assertEqual(response.status_code, 201)

        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(message, "Skill activated successfully.")
        self.assertEqual(data, {
            "Skill_ID": 1,
            "Skill_Is_Active": True,
            "Skill_Name": "Basic programming 1"
        })

    def test_deactivateSkillNotFound(self):
        response = self.client.put('/skill/toggle/100')
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, "Skill does not exist.")

class TestRoleR(TestApp):
    # read methods
    def test_getAllRoles(self):
        response = self.client.get('/role')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, [
            {'Role_Desc': 'Software Engineer','Role_ID': 1,'Role_Is_Active': True,'Role_Name': 'SWE'},
            {'Role_Desc': 'Project Manager','Role_ID': 2,'Role_Is_Active': True,'Role_Name': 'PM'},
            {'Role_Desc': 'Business Analyst','Role_ID': 3,'Role_Is_Active': False,'Role_Name': 'BA'}
        ])

class TestRoleC(TestApp):
    # create methods
    def test_createRole(self):
        response = self.client.post('/role/create', json={'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 4, 'Role_Is_Active': True, 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})

    def test_createRoleEmptyName(self):
        response = self.client.post('/role/create', json={'Role_Name': '', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be empty.")

        response = self.client.post('/role/create', json={'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be empty.")

    def test_createRoleNameBorder50Character(self):
        response = self.client.post('/role/create', json={'Role_Name': 't' * 50, 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 4, 'Role_Is_Active': True, 'Role_Name': 't' * 50, 'Role_Desc': 'testDesc'})

        response = self.client.post('/role/create', json={'Role_Name': 't' * 51, 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be more than 50 characters.")

    def test_createRoleAlreadyExists(self):
        response = self.client.post('/role/create', json={'Role_Name': 'SWE', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role already exists.")

    def test_createRoleEmptyDesc(self):
        # empty desc is allowed
        response = self.client.post('/role/create', json={'Role_Name': 'testRole1', 'Role_Desc': ''})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 4, 'Role_Is_Active': True, 'Role_Name': 'testRole1', 'Role_Desc': ''})

        response = self.client.post('/role/create', json={'Role_Name': 'testRole2'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 5, 'Role_Is_Active': True, 'Role_Name': 'testRole2', 'Role_Desc': ''})

    def test_createRoleDescBorder255Character(self):
        response = self.client.post('/role/create', json={'Role_Name': 'testRole1', 'Role_Desc': 't' * 255})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 4, 'Role_Is_Active': True, 'Role_Name': 'testRole1', 'Role_Desc': 't' * 255})

        response = self.client.post('/role/create', json={'Role_Name': 'testRole2', 'Role_Desc': 't' * 256})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role description cannot be more than 255 characters.")

    def test_createRoleNumericName(self):
        response = self.client.post('/role/create', json={'Role_Name': '123', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be numeric.")
    
    def test_createRoleNumericDesc(self):
        response = self.client.post('/role/create', json={'Role_Name': 'testRole', 'Role_Desc': '123'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role description cannot be numeric.")

# to be implemented next
class TestRoleU(TestApp):
    # update methods
    def test_updateRole(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})

    def test_updateRoleEmptyName(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': '', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be empty.")

        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be empty.")

    # should never happen with the front end
    def test_updateRoleEmptyID(self):
        response = self.client.put('/role/update', json={'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID cannot be empty.")
    
    # should never happen given the front end
    def test_updateRoleIDNotFound(self):
        response = self.client.put('/role/update', json={'Role_ID': 100, 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID not found.")

    # should never happen given the front end
    def test_updateRoleIDNotInteger(self):
        response = self.client.put('/role/update', json={'Role_ID': 'a', 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID must be an integer.")

        response = self.client.put('/role/update', json={'Role_ID': '', 'Role_Name': 'testRole', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID must be an integer.")

    def test_updateRoleNameBorder50Character(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 't' * 50, 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 't' * 50, 'Role_Desc': 'testDesc'})

        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 't' * 51, 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be more than 50 characters.")

    def test_updateRoleAlreadyExists(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'BA', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role already exists.")

    def test_updateRoleEmptyDesc(self):
        # empty desc is allowed
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole1', 'Role_Desc': ''})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 'testRole1', 'Role_Desc': ''})

        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole2'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 'testRole2', 'Role_Desc': ''})

    def test_updateRoleDescBorder255Character(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole1', 'Role_Desc': 't' * 255})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 'testRole1', 'Role_Desc': 't' * 255})

        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole2', 'Role_Desc': 't' * 256})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role description cannot be more than 255 characters.")

    def test_updateRoleNumericName(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': '123', 'Role_Desc': 'testDesc'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role name cannot be numeric.")
    
    def test_updateRoleNumericDesc(self):
        response = self.client.put('/role/update', json={'Role_ID': 1, 'Role_Name': 'testRole', 'Role_Desc': '123'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role description cannot be numeric.")

class TestRoleD(TestApp):
    # delete methods
    def test_deactivateRole(self):
        response = self.client.put('/role/toggle/1')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': False, 'Role_Name': 'SWE', 'Role_Desc': 'Software Engineer'})

        response = self.client.put('/role/toggle/1')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Role_ID': 1, 'Role_Is_Active': True, 'Role_Name': 'SWE', 'Role_Desc': 'Software Engineer'})

    def test_deactivateRoleNotFound(self):
        response = self.client.put('/role/toggle/100')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role does not exist.")

class TestDeleteLJ(TestApp):
    def test_deleteLJ(self):
        response = self.client.get('/LJ/deleteLJ/1')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Learning Journey deleted successfully.")

    def test_deleteLJNotFound(self):
        response = self.client.get('/LJ/deleteLJ/50')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Learning Journey does not exist.")

class TestDeleteCourse(TestApp):
    def test_deleteCourse(self):
        response = self.client.get('/course/delete/IS-1/1')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Course deleted successfully.")

    def test_deleteLastCourse(self):
        response = self.client.get('/course/delete/IS-5/6')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Cannot delete course. At least one course is required.")

    def test_deleteNullCourse(self):
        response = self.client.get('/course/delete/IS-10/6')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Cannot delete course. Learning Journey with Course selected does not exist.")

    def test_deleteNullLJ(self):
        response = self.client.get('/course/delete/IS-1/6')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)['message']
        self.assertEqual(data, "Cannot delete course. Learning Journey with Course selected does not exist.")

class TestAssignRoleFromSkill(TestApp):
    """POST /skill/assign_to_role"""

    def test_assignOneRoleFromSkill(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': 3})
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Skill_ID': 1, 'Role_ID': 3})
        self.assertEqual(message, "Role(s) assigned to Skill successfully.")

    def test_assignManyRolesFromSkill(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': [3, 2]})
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(data, [{'Role_ID': 3, 'Skill_ID': 1}, {'Role_ID': 2, 'Skill_ID': 1}])
        self.assertEqual(message, "Role(s) assigned to Skill successfully.")

    def test_assignRoleFromSkillMissingSkillKey(self):
        response = self.client.post('/skill/assign_to_role', json={'Role_ID': 3})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_assignRoleFromSkillMissingRoleKey(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")
    
    def test_assignRoleFromSkillSkillIDNotInteger(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 'a', 'Role_ID': 3})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_assignRoleFromSkillRoleIDNotIntegerOrList(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': 'a'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_assignRoleFromSkillRoleIDEmptyList(self):
        response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': []})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID cannot be empty list")

    # enable of FK constraint on sqllite not working, so this test will fail
    # works as intended on postman with sql server
    # def test_assignRoleFromSkillSkillIDOutOfRange(self):
    #     response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 9999, 'Role_ID': 3})
    #     self.assertEqual(response.status_code, 500)
    #     message = json.loads(response.data)['message']
    #     self.assertIn(message, "Unable to assign skill to role. Error message: ")

    # enable of FK constraint on sqllite not working, so this test will fail
    # works as intended on postman with sql server
    # def test_assignRoleFromSkillRoleIDOutOfRange(self):
    #     response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': 9999})
    #     self.assertEqual(response.status_code, 500)
    #     message = json.loads(response.data)['message']
    #     self.assertIn(message, "Unable to assign skill to role. Error message: ")

    # UNIQUE constraint failed on sql lite, so this test will fail
    # works as intended on postman with sql server
    # def test_assignRoleFromSkillAlreadyAssigned(self):
    #     response = self.client.post('/skill/assign_to_role', json={'Skill_ID': 1, 'Role_ID': 1})
    #     self.assertEqual(response.status_code, 500)
    #     message = json.loads(response.data)['message']
    #     self.assertIn(message, "Unable to assign skill to role. Error message: ")


class TestUnassignRoleFromSkill(TestApp):
    """DELETE /skill/unassign_role_from_skill"""
    def test_unassignRoleFromSkill(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 1, 'Role_ID': 1})
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(data, {'Skill_ID': 1, 'Role_ID': 1})
        self.assertEqual(message, "Role unassigned from skill successfully.")

    def test_unassignManyRoleFromSkill(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 2, 'Role_ID': [1, 2]})
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)['message']
        data = json.loads(response.data)['data']
        self.assertEqual(data, [{'Skill_ID': 2, 'Role_ID': 1}, {'Skill_ID': 2, 'Role_ID': 2}])
        self.assertEqual(message, "Role unassigned from skill successfully.")

    def test_unassignRoleFromSkillMissingSkillKey(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Role_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_unassignRoleFromSkillMissingRoleKey(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_unassignRoleFromSkillSkillIDNotInteger(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 'a', 'Role_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_unassignRoleFromSkillRoleIDNotInteger(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 1, 'Role_ID': 'a'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill ID and Role ID cannot be empty or non interger")

    def test_unassignRoleFromSkillRoleIDEmptyList(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 1, 'Role_ID': []})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Role ID cannot be empty list")

    def test_unassignRoleFromSkillRoleNotFound(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 1, 'Role_ID': 9999})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill and role does not exist.")

    def test_unassignRoleFromSkillSkillNotFound(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 9999, 'Role_ID': 1})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill and role does not exist.")

    def test_unassignManyRoleFromSkillRoleNotFound(self):
        response = self.client.delete('/skill/unassign_role_from_skill', json={'Skill_ID': 2, 'Role_ID': [999]})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill and role does not exist.")



    



    pass
    # roleID not in table
    # skillID not in table ect ect

class TestAssignCourseFromSkill(TestApp):
    """POST /skill/assign_to_courses"""
    pass

class TestUnassignCourseFromSkill(TestApp):
    """DELETE /skill/unassign_course_from_skill"""
    pass

class TestGetAssignedRolesFromSkill(TestApp):
    """GET /skill/assigned_roles""" # split this into 2 classes?
    """GET /skill/get_assigned_roles_by_ID/<int:skill_id>"""
    pass

class TestGetAssignedCoursesFromSkill(TestApp):
    """GET /skill/assigned_courses"""  # split this into 2 classes?
    """GET /skill/get_assigned_courses_by_ID/<int:skill_id>"""
    pass

"""
WIP
assign and unassign skills to roles and courses from skill 
(4 of them, 3 more to do)

get assigned role from skillID

get assigned role from ONE skillID

get assigned course from skillID

get assigned course from ONE skillID

LJ and all its related end points


"""

if __name__ == '__main__':
    unittest.main()
