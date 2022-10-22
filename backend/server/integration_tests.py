from email import message
import unittest
import flask_testing
import json

from flaskServer import *

import os
from dotenv import load_dotenv
load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if DB_USERNAME is None or DB_PASSWORD is None:
    print('DB_USERNAME or DB_PASSWORD not set')
    exit(1)


class TestApp(flask_testing.TestCase):
    """
    Intergration tests for the flask server
    Using ../sql/createTables.sql and ../sql/insertDataSetA.sql
    to create a test database and populate it with data
    """
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,'pool_recycle': 280}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        with open('../sql/createTables.sql') as f:
            for statement in f.read().split(';'):
                stm = statement.replace("is212_G1T1", "is212_G1T1_test")
                db.session.execute(stm.strip() + ';') if len(stm.strip()) > 0 else None

        with open('../sql/insertDataSetA.sql') as f:
            for statement in f.read().split(';'):
                stm = statement.replace("is212_G1T1", "is212_G1T1_test")
                db.session.execute(stm.strip() + ';') if len(stm.strip()) > 0 else None

    def tearDown(self):
        # not sure why the database is empty if we dont drop it
        db.session.execute('DROP DATABASE is212_G1T1_test;')


class TestSkillCRUD(TestApp):

    # read methods
    def test_getSkills(self):
        response = self.client.get('/skill')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']

        self.assertEqual(data[0], {'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 1'})
        self.assertEqual(data, [{'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 1'}, {'Skill_ID': 2, 'Skill_Is_Active': True, 'Skill_Name': 'Basic programming 2'}, {'Skill_ID': 3, 'Skill_Is_Active': True, 'Skill_Name': 'Intermediate programming 1'}, {'Skill_ID': 4, 'Skill_Is_Active': True, 'Skill_Name': 'Intermediate programming 2'}, {'Skill_ID': 5, 'Skill_Is_Active': True, 'Skill_Name': 'Modeling 1'}, {'Skill_ID': 6, 'Skill_Is_Active': True, 'Skill_Name': 'Agile 1'}, {'Skill_ID': 7, 'Skill_Is_Active': True, 'Skill_Name': 'Critical thinking 1'}, {'Skill_ID': 8, 'Skill_Is_Active': True, 'Skill_Name': 'Database 1'}, {'Skill_ID': 9, 'Skill_Is_Active': True, 'Skill_Name': 'Front end 1'}, {'Skill_ID': 10, 'Skill_Is_Active': True, 'Skill_Name': 'Business process management 1'}, {'Skill_ID': 11, 'Skill_Is_Active': False, 'Skill_Name': 'Prototyping 1'}])

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

    # update methods
    def test_updateSkill(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 1, 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)['data']
        message = json.loads(response.data)['message']
        self.assertEqual(data, {'Skill_ID': 1, 'Skill_Is_Active': True, 'Skill_Name': 'testSkill'})
        self.assertEqual(message, "Skill updated successfully.")

    def test_updateSkillNotFound(self):
        response = self.client.put('/skill/update', json={'Skill_ID': 100, 'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 500)

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

class TestRoleCRUD(TestApp):

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

    # update methods
    
    # not implemented

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

    
if __name__ == '__main__':
    unittest.main()
