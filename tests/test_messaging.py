import unittest

from my_classes.MessagingService import MessagingService


class Test(unittest.TestCase):

    def test_list_int(self):
        service=MessagingService("Jsondata/Messages.json")
        result=service._load_messages()
        self.assertIsNot(result,bool)

if __name__ == '__main__':
    unittest.main()