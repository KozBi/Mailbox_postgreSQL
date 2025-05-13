from my_classes.MessagingService import MessagingService
from my_classes.UserCommandHandler import UserCommandHandler
from datetime import datetime

class CommandRouter:
    def __init__(self, Version,Creationdate):
        self.Version=Version
        self.Creationdate=Creationdate
        self.UserCommandHandler= UserCommandHandler()
        self.MessagingService=MessagingService()

    
    def _help(self):
        return {"help":"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n" 
        f"{self.UserCommandHandler.status()}\n"
        "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n" 
        "Available command:\n"
        "'uptime'-return life time of server\n"
        "'info'-informs about server version\n"
        "'stop'-close the server\n"
        "'login |your_login| login to your account.\n"
        "'logout' you logout from your account\n"
        "'create |login password| - a new account create with a passowrd\n"
        "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n" 
        " |Commands  If you are LOGIN IN |\n"
        "'msg' check how many messages you have\n" 
        "'wrt' write a message to another user\n" 
        "'rd' read all message\n" 
        "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n" 
        }

    def handle_command(self,cmd):
        self.UserCommandHandler.status()
        # hanlde commands from class User
        # if login add also information how many messages already loged user has.
        user_respond= self.UserCommandHandler.handle_user_command(cmd)
        if user_respond and self.UserCommandHandler.UserMenager.logged_user:
            return f"{user_respond}, You have {self.MessagingService.check_num_message(self.UserCommandHandler.UserMenager.logged_user)} mesagges"
        if user_respond:
            return user_respond
        
        # hanlde commands from class Messages
        message_respond=self.MessagingService.handel_message_command(cmd, self.UserCommandHandler.UserMenager.logged_user)
        if message_respond:
            return message_respond
        
        match str(cmd):
            case "uptime": 
                #calcute server date
                current_time=datetime.now()
                current_time=current_time-self.Creationdate
                current_time= str(current_time).split('.')[0]
                return f"Server uptime: {current_time}"
            case "info": 
                return f"Server version: {self.Version}"
            case "help": 
                    return self._help()
            case "stop": 
                pass
            case _: #deafult case
                return "Uknown command, try 'help'"