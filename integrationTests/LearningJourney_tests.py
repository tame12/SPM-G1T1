import unittest
import flask_testing
import json
import sys  
# append the path of the
sys.path.append("..")
  
# module
from backend.server.flaskServer import *

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

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
            SkillCourse(Course_ID="IS-2", Skill_ID=3),
            SkillCourse(Course_ID="IS-11", Skill_ID=1),


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

class TestCreateLJ(TestApp):
    def test_createLJ_success(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 3,
            "Staff_ID": 3,
            "LJ_Number": 4,
            "LJ_Courses": ["IS-6","IS-11","IS-7"],
            "LJ_Skills":[1,2,3]
        })

        expected_data_response = {
            "LJ_ID": 7,
            "LJ_Number": 4,
            "Role_ID": 3,
            "Staff_ID": 3
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'LJ created successfully.')
        self.assertEqual(response.json['data'], expected_data_response)

    def test_createLJ_fail_invalid_keys(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 4,
            "Staff_ID": 999
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Fields must match "Role_ID","Staff_ID","LJ_Number","LJ_Courses" .')

    def test_createLJ_fail_empty_keys(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 3,
            "Staff_ID": 3,
            "LJ_Number": 4,
            "LJ_Courses": [],
            "LJ_Skills":[]
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Fields cannot be empty')

    
    def test_createLJ_fail_invalid_staffID(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 4,
            "Staff_ID": 9999,
            "LJ_Number": 4,
            "LJ_Courses": ["IS-6","IS-11","IS-7"],
            "LJ_Skills":[1,2,3]
        })


        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Staff does not exist')

    def test_createLJ_fail_invalid_roleID(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 99999,
            "Staff_ID": 3,
            "LJ_Number": 4,
            "LJ_Courses": ["IS-6","IS-11","IS-7"],
            "LJ_Skills":[1,2,3]
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Role does not exist')

    # Unsure of whether I should be doing this or not
    # def test_createLJ_fail_invalid_LJCourse_and_LJSkills_not_matching(self):
    #     response = self.client.post('/LJ/addLJ', json={
    #         "Role_ID": 99999,
    #         "Staff_ID": 3,
    #         "LJ_Number": 4,
    #         "LJ_Courses": ["IS-6","IS-11","IS-7"],
    #         "LJ_Skills":[1,2,3]
    #     })

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json['message'], 'Role does not exist')

    # test create LJ fail because LJ already exists
    def test_createLJ_fail_LJ_already_exists(self):
        response = self.client.post('/LJ/addLJ', json={
            "Role_ID": 1,
            "Staff_ID": 1,
            "LJ_Number": 1,
            "LJ_Courses": ["IS-1","IS-2"],
            "LJ_Skills":[1,2]
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'LJ already exists.')

class TestViewLJ_Learner(TestApp):
    def test_view_LJ_learner(self):
        # Tests if "John Smith", a learner, is able to view his courses
        response = self.client.get('/LJ/1')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        expected_data_response = [{'LJ_ID': 1, 'LJ_Number': 1, 'Role_ID': 1, 'Staff_ID': 1}, {'LJ_ID': 2, 'LJ_Number': 2, 'Role_ID': 2, 'Staff_ID': 1}, {'LJ_ID': 3, 'LJ_Number': 3, 'Role_ID': 3, 'Staff_ID': 1}]

        self.assertEqual(data, expected_data_response)

        expected_role_data_response = [{'Role_ID': 1, 'Role_Name': 'SWE', 'Role_Desc': 'Software Engineer', 'Role_Is_Active': 1}, {'Role_ID': 2, 'Role_Name': 'PM', 'Role_Desc': 'Project Manager', 'Role_Is_Active': 1}, {'Role_ID': 3, 'Role_Name': 'BA', 'Role_Desc': 'Business Analyst', 'Role_Is_Active': 0}]
        self.assertEqual(json.loads(response.data)['role_data'], expected_role_data_response)

    def test_view_LJ_learner_invalid(self):
        # Tests a learner that does not exist
        response = self.client.get('/LJ/999')
        self.assertEqual(response.status_code, 404)

class TestGetCoursesByLJ_ID(TestApp):
    def test_get_courses_by_lj_id_success(self):
        response = self.client.get('LJ/get_courses_by_LJ_ID/1')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data'], [
        {
            "Course_Category": "Technical",
            "Course_Desc": "case aborum.",
            "Course_ID": "IS-1",
            "Course_Is_Active": True,
            "Course_Name": "Information Systems & Innovation",
            "Course_Type": "Internal"
        },
        {
            "Course_Category": "Technical",
            "Course_Desc": "modeling, lorem ipsum doloraborum.",
            "Course_ID": "IS-2",
            "Course_Is_Active": True,
            "Course_Name": "Business Process Analysis and Solutioning",
            "Course_Type": "External"
        }
    ])

    def test_get_courses_by_lj_id_fail_invalid_lj_id(self):
        response = self.client.get('LJ/get_courses_by_LJ_ID/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'LJ does not exist')

class TestGetAllLJ(TestApp):
    def test_get_all_LJ(self):
        response = self.client.get('/LJ')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data'], [{'LJ_ID': 1, 'LJ_Number': 1, 'Role_ID': 1, 'Staff_ID': 1}, {'LJ_ID': 2, 'LJ_Number': 2, 'Role_ID': 2, 'Staff_ID': 1}, {'LJ_ID': 3, 'LJ_Number': 3, 'Role_ID': 3, 'Staff_ID': 1}, {'LJ_ID': 4, 'LJ_Number': 1, 'Role_ID': 1, 'Staff_ID': 4}, {'LJ_ID': 5, 'LJ_Number': 2, 'Role_ID': 2, 'Staff_ID': 4}, {'LJ_ID': 6, 'LJ_Number': 3, 'Role_ID': 3, 'Staff_ID': 4}])

class TestAddCourseToLJ(TestApp):

    def test_add_course_to_lj_sucess(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_ID": 2, 
            "Course_ID": "IS-1",
            "Skill_ID": 2
        })

        expected_response = {'Course_ID': 'IS-1', 'LJ_ID': 2, 'Skill_ID': '2'}
        self.assertEqual(response.json['data'], expected_response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Course added successfully.')

    def test_add_course_to_lj_fail_skill_unmapped(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_ID": 1,
            "Course_ID": "IS-3",
            "Skill_ID": 3
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Skill is not mapped to course.')


    def test_add_course_to_lj_fail_invalid_keys(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_IDa": 1,
            "Course_IDa": "IS-1",
            "Skill_IDa": 2
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Fields must match "LJ_ID","Course_ID","Skill_ID"')

    def test_add_course_to_lj_fail_empty_values(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_ID": "",
            "Course_ID": "IS-1",
            "Skill_ID": 2
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Fields cannot be empty')

    def test_add_course_to_lj_fail_lj_already_exists(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_ID": 1,
            "Course_ID": "IS-1",
            "Skill_ID": 1
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Course already exists in the LJ.')

    def test_add_course_to_lj_fail_skill_not_mapped_to_role(self):
        response = self.client.post('/LJ/addLJ/Course', json={
            "LJ_ID": 3,
            "Course_ID": "IS-1",
            "Skill_ID": 1
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Skill is not mapped to role.')

class TestgetCoursesAndSkillByLLJID(TestApp):
    def test_get_courses_and_skill_by_LJ_ID_success(self):
        response = self.client.get('/LJ/getCourseAndSkillByLJ_ID/1')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data'], [{'Course_ID': 'IS-1', 'Course_Name': 'Information Systems & Innovation', 'Skill_ID': 1, 'Skill_Name': 'Basic programming 1'}, {'Course_ID': 'IS-2', 'Course_Name': 'Business Process Analysis and Solutioning', 'Skill_ID': 2, 'Skill_Name': 'Basic programming 2'}])

    def test_get_courses_and_skill_by_LJ_ID_fail_invalid_lj_id(self):
        response = self.client.get('/LJ/getCourseAndSkillByLJ_ID/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'LJ does not exist')
        
if __name__ == '__main__':
    unittest.main()
