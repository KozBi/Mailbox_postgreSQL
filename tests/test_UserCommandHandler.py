import unittest
import tempfile
import json
import os
from my_classes.UserCommandHandler import UserCommandHandler

class TestUserCommandHandler(unittest.TestCase):

    def setUp(self):
        #create temporary file with a example users
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        json.dump([{"id": 1, "username": "bob"}], self.temp_file)
        self.temp_file.close()

        #overwrite Users.json with a temporary file
        self.UCH=UserCommandHandler()
        self.UCH.UserMenager.userfile=self.temp_file.name


    def tearDown(self):
        # Delte file after test function
        os.remove(self.temp_file.name)

    def test_handle_user_command(self):
        
        result=self.UCH.handle_user_command("create user password123")
        self.assertIsInstance(result,str)
