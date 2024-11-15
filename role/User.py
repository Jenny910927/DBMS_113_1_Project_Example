from action.Exit import Exit
from action.CreateEvent import CreateEvent
from action.ListEvent import ListEvent
from action.ModifyUserInfo import ModifyUserInfo
from .Role import Role

class User(Role):
    def __init__(self, userid, username, pwd, email, isUser, isAdmin):
        self.userid = userid
        self.username = username
        self.pwd = pwd
        self.email = email
        self.isUser = isUser
        self.isAdmin = isAdmin
        self.action_dict = {
            '1': CreateEvent("Create Study Event"),
            '2': ListEvent("List All Available Study Events"),
            # '3': JoinEvent("Join Study Event"),
            '4': ModifyUserInfo("Modify User Info"),
            # '5': Logout("Logout"),
            '6': Exit("Leave System")
        }
        print(f'Create user | userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}')

    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}'
    def get_username(self):
        return self.username
    

    def list_action(self):
        msg = ''
        for key in self.action_dict:
            msg = msg + f'[{key}] {self.action_dict[key].get_name()}\n'
        return msg
    
    