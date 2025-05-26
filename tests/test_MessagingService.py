import unittest
import tempfile
import json
import os

from my_classes.MessagingService import MessagingService
from my_classes.UserMenager import UserMenager

class Test(unittest.TestCase):

    def setUp(self):
        #create object but json file is a test file
        self.service=MessagingService("tests/fixtures/test_Messages.json")
        self.user=UserMenager()
        # file is only read, not temporary file requiered
        self.user.userfile="tests/fixtures/test_Users.json"

        #create temporary file with a messages
        with open("tests/fixtures/test_Messages.json", 'r',encoding='utf-8') as f:
            data=json.load(f)
        self.temp_file_msg = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        json.dump(data, self.temp_file_msg)
        self.temp_file_msg.close()

        self.service.f_message=self.temp_file_msg.name

    def tearDown(self):      
        # Delte file after test function
        os.remove(self.temp_file_msg.name)

    def test_number_of_messages(self):   
        #max messages
        result=self.service.number_message(1)
        self.assertIn(result,"You have 5 messages. Your box messages is full. Please delete messages using del command")

        #1 message
        result=self.service.number_message(2)
        self.assertIn(result,"You have 1 messages")
        
        #no message
        result=self.service.number_message(3)
        self.assertIn(result,"You have 0 messages")

    def test_read_message_all(self):

        #max messages
        self.user.logged_user='admin'
        self.user.logged_user_id=1
        result=self.service.handle_message_command("rd",self.user)
        self.assertIn("Your's box messages is full. Please delete messages using del command",result)

        #1 message
        self.user.logged_user='bob'
        self.user.logged_user_id=2
        result=self.service.handle_message_command("rd",self.user)
        self.assertIn("hello bob it's admin",result)

        #no message
        self.user.logged_user='adam3'
        self.user.logged_user_id=3
        result=self.service.handle_message_command("rd",self.user)
        self.assertIn(result,"You dont have any messages")

    def test_write_and_read_message(self):

        #login as a bob for a tests
        self.user.logged_user='bob'
        self.user.logged_user_id=2

        #write a new message
        result=self.service.handle_message_command("w adam3",self.user)
        self.assertIn("found, please type a message --- max 255 of characters",result)
        result=self.service.handle_message_command("Test new message xyz",self.user)
        self.assertIn(result,"Message sent")

        #login as a bob for a tests
        self.user.logged_user='adam3'
        self.user.logged_user_id=3

        #check if messages is saved
        result=self.service.handle_message_command("rd",self.user)
        self.assertIn("Test new message xyz",result)

    def test_delete_message(self):
        #login as a bob for a tests
        self.user.logged_user='bob'
        self.user.logged_user_id=2

        #no message number specified
        result=self.service.handle_message_command("del",self.user)
        self.assertIn("Wrong parameter",result)

        #delete 1 message
        result=self.service.handle_message_command("del 2",self.user)
        self.assertIn("Message 2 has been deleted",result)

        #no message number specified
        result=self.service.handle_message_command("del -a",self.user)
        self.assertIn("All messages has been deleted",result)

    
    def test_admin_rd(self):
        #login as a admin for a tests
        self.user.logged_user='admin'
        self.user.logged_user_id=1
        self.user.logged_admin=True

        result=self.service.handle_message_command("admin_rd bob",self.user)
        self.assertIn("hello bob it's admin",result)

        result=self.service.handle_message_command("admin_rd adam3",self.user)
        
        self.assertIn("You dont have any messages",result)

        result=self.service.handle_message_command("admin_rd xyz",self.user)
        self.assertIn("Please eneter correct username ",result)

        result=self.service.handle_message_command("admin_rd",self.user)
        self.assertIn("Please eneter username ",result)

    def test_admin_del(self):
        #login as a admin for a tests
        self.user.logged_user='admin'
        self.user.logged_user_id=1
        self.user.logged_admin=True

        result=self.service.handle_message_command("admin_del admin 1",self.user)
        self.assertIn("Message 1 has been deleted",result)

        result=self.service.handle_message_command("admin_del bob -a",self.user)
        self.assertIn("All messages has been deleted",result)

        result=self.service.handle_message_command("admin_del xyz -a",self.user)
        self.assertIn("This user doesn't exist",result)

        result=self.service.handle_message_command("admin_del bob",self.user)
        self.assertIn("['-a' delete all message]",result)
    
if __name__ == '__main__':
    unittest.main()