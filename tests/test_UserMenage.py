import unittest
import tempfile
import json
import os
from my_classes.UserCommandHandler import UserCommandHandler

class TestUserMenage(unittest.TestCase):

    def setUp(self):
        #create temporary file with a example users
        with open("tests/fixtures/test_Users.json", 'r',encoding='utf-8') as f:
            data=json.load(f)
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        json.dump(data, self.temp_file)
        self.temp_file.close()

        #create temporary file with a example passwords
        with open("tests/fixtures/test_Passwords.json", 'r',encoding='utf-8') as f:
            data=json.load(f)
        self.temp_file_pw = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        json.dump(data, self.temp_file_pw)
        self.temp_file_pw.close()

        #overwrite Users.json with a temporary file
        self.UCH=UserCommandHandler()
        self.UCH.UserMenager.userfile=self.temp_file.name
        self.UCH.UserMenager.passfile=self.temp_file_pw.name


    def tearDown(self):
        
        
        # Delte file after test function
        os.remove(self.temp_file.name)
        os.remove(self.temp_file_pw.name)

    
    def test_get_user_id(self):
        
        result1=self.UCH.UserMenager.get_user_by_id(1)
        self.assertEqual(result1,"admin")

        result2=self.UCH.UserMenager.get_user_by_id(2)
        self.assertEqual(result2,"bob")

        result3=self.UCH.UserMenager.get_id_by_user("admin")
        self.assertEqual(result3,"1")

        result4=self.UCH.UserMenager.get_id_by_user("bob")
        self.assertEqual(result4,"2")


    def test_handle_user_command_create_user(self):

        #create user
        result=self.UCH.handle_user_command("create user123 password123")
        self.assertTrue(self.UCH.UserMenager.pending_cr_user)
        self.assertTrue(self.UCH.UserMenager.pending_cr_user_id)
        self.assertIn(self.UCH.UserMenager.pending_cr_password, "password123")
        self.assertIn(result,"Please insert password once again to confirm your password")
        
        result2=self.UCH.handle_user_command("password123")
        self.assertIn("created successfully.",result2)

        result3=self.UCH.UserMenager.get_user_by_id(4)
        self.assertEqual(result3,"user123")

        result4=self.UCH.UserMenager.get_id_by_user("user123")
        self.assertEqual(result4,"4")

    def test_check_login_admin_and_fct(self):

        #check admin login
        result1=self.UCH.handle_user_command("login admin")
        self.assertTrue(self.UCH.UserMenager.pending_admin)
        self.assertTrue(self.UCH.UserMenager.pending_user)
        self.assertEqual(self.UCH.UserMenager.pending_user_id,1)
        self.assertIn(result1,"You are trying login as an admin, please insert password")

        #check admin password
        result1=self.UCH.handle_user_command("admin")
        self.assertTrue(self.UCH.UserMenager.logged_admin)
        self.assertTrue(self.UCH.UserMenager.logged_user_id)
        self.assertIn("You are logged in as admin",result1)

        #check user list
        result2=self.UCH.handle_user_command("admin_user")
        self.assertIn("admin",result2)
        self.assertIn("bob",result2)
        self.assertIn("adam3",result2)



    def test_check_login_logout_normal_user(self):

        #check existing user
        result2=self.UCH.handle_user_command("login bob")
        self.assertTrue(self.UCH.UserMenager.pending_user)
        self.assertEqual(self.UCH.UserMenager.pending_user_id,2)
        self.assertIn(result2,"Login found, please insert password")

        #check bob password
        result1=self.UCH.handle_user_command("adam2")
        self.assertTrue(self.UCH.UserMenager.logged_user)
        self.assertTrue(self.UCH.UserMenager.logged_user_id)
        self.assertIn("You are logged in as bob",result1)

        result2=self.UCH.handle_user_command("logout")
        self.assertFalse(self.UCH.UserMenager.logged_user)
        self.assertFalse(self.UCH.UserMenager.logged_user_id)
        self.assertIn("User succesfully logout",result2)


    def test_check_login_not_existing_user(self):

        #check not exisiting user
        result3=self.UCH.handle_user_command("login xyz")
        self.assertFalse(self.UCH.UserMenager.pending_user)
        self.assertFalse(self.UCH.UserMenager.pending_user_id)
        self.assertIn(result3,"User doesn't exist")
        
    def test_check_login_inncorect_password(self):

        #check exisiting user
        result=self.UCH.handle_user_command("login adam3")
        self.assertTrue(self.UCH.UserMenager.pending_user)
        self.assertTrue(self.UCH.UserMenager.pending_user_id)
        self.assertIn(result,"Login found, please insert password")

        #check inccorect
        result1=self.UCH.handle_user_command("xxxzxzx")
        self.assertFalse(self.UCH.UserMenager.logged_user)
        self.assertFalse(self.UCH.UserMenager.logged_user_id)
        self.assertIn("Incorrect password",result1)

    def test_change_password(self):

        #check exisiting user
        result=self.UCH.handle_user_command("login adam3")
        self.assertTrue(self.UCH.UserMenager.pending_user)
        self.assertTrue(self.UCH.UserMenager.pending_user_id)
        self.assertIn(result,"Login found, please insert password")

        #check login
        result1=self.UCH.handle_user_command("adam3")
        self.assertTrue(self.UCH.UserMenager.logged_user)
        self.assertTrue(self.UCH.UserMenager.logged_user_id)
        self.assertIn("You are logged in as adam3",result1)

        result2=self.UCH.handle_user_command("pw_change new_passoword")
        self.assertIn("Please enter password once again",result2)

        result3=self.UCH.handle_user_command("new_passoword")
        self.assertIn("Password has been changed" ,result3)

        #logout for test new password
        self.UCH.handle_user_command("logout")

        #login with a new password
        self.UCH.handle_user_command("login adam3")
        result = self.UCH.handle_user_command("new_passoword")
        self.assertIn("You are logged in as adam3", result)

    def test_status(self):

        result=self.UCH.UserMenager.status()
        self.assertIn("You are not logged in, please type your login and password",result)

        #check exisiting user
        result=self.UCH.handle_user_command("login adam3")
        self.assertTrue(self.UCH.UserMenager.pending_user)
        self.assertTrue(self.UCH.UserMenager.pending_user_id)
        self.assertIn(result,"Login found, please insert password")

        #check login
        result1=self.UCH.handle_user_command("adam3")
        self.assertTrue(self.UCH.UserMenager.logged_user)
        self.assertTrue(self.UCH.UserMenager.logged_user_id)
        self.assertIn("You are logged in as adam3",result1)

        result=self.UCH.UserMenager.status()
        self.assertIn("You are already logged in as adam3",result)

