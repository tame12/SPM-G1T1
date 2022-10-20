from email import message
import unittest
import flask_testing
import json
# import sys

# from backend.server.flaskServer import *
from sqlalchemy import text

# import sys
# sys.path.insert(1, '../server')

from flaskServer import *

import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if DB_USERNAME is None or DB_PASSWORD is None:
    print('DB_USERNAME or DB_PASSWORD not set')
    exit(1)

# someone pls send help
# need to automate the creation of the test database and not use production db
# need to set up and tear down database as the test for get skills and create skills will interfere with each other
# kinda working when manually loading production DB with createTables.sql and insertDataSetA.sql

# WARNING DO NOT RUN THIS FILE AS IT IS USING PRODUCTION DB
exit()
# RUN AT YOUR OWN RISK

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/is212_g1t1'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,'pool_recycle': 280}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        # with open('../sql/createTables.sql') as f:
        #     db.engine.execute(text(f.read()))
        #     print(text(f.read()))
        # with open('../sql/insertDataSetA.sql') as f:
        #     db.engine.execute(text(f.read()))
        # db.create_all()
        pass

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

class TestSkill(TestApp):

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

    def test_createSkillAlreadyExists(self):
        response = self.client.post('/skill/create', json={'Skill_Name': 'Basic programming 1'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill already exists.")

    # update methods
    def test_updateSkillNotFound(self):
        response = self.client.put('/skill/100', json={'Skill_Name': 'testSkill'})
        self.assertEqual(response.status_code, 404)

    def test_updateSkillAlreadyExists(self):
        response = self.client.put('/skill/update', json={"Skill_ID": 1, 'Skill_Name': 'Basic programming 2'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Skill name already exists.")

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

    # def test_postSkill(self):
    #     response = self.client.post('/skill', json={'name': 'C++', 'description': 'C++ is a programming language'})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json, {'id': 3, 'name': 'C++', 'description': 'C++ is a programming language'})

    # def test_postSkillAlreadyExists(self):
    #     response = self.client.post('/skill', json={'name': 'Python', 'description': 'Python is a programming language'})
    #     self.assertEqual(response.status_code, 409)

    # def test_postSkillMissingName(self):
    #     response = self.client.post('/skill', json={'description': 'Python is a programming language'})
    #     self.assertEqual(response.status_code, 400)

    # def test_postSkillMissingDescription(self):
    #     response = self.client.post('/skill', json={'name': 'Python'})
    #     self.assertEqual(response.status_code, 400)

    # def test_putSkill(self):
    #     response = self.client.put('/skill/1', json={'name': 'Python', 'description': 'Python is a programming language'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {'id': 1, 'name': 'Python', 'description': 'Python is a programming language'})

    # def test_putSkillNotFound(self):
    #     response = self.client.put('/skill/100', json={'name': 'Python', 'description': 'Python is a programming language'})
    #     self.assertEqual(response.status_code, 404)

    # def test_putSkillMissingName(self):
    #     response = self.client.put('/skill/1', json={'



if __name__ == '__main__':
    unittest.main()
