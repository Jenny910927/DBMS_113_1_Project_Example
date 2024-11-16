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

    def get_info_msg_no_pwd(self):
        return f'userid: {self.userid}, username: {self.username}, email: {self.email}'
    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}'
    def get_username(self):
        return self.username
    def get_userid(self):
        return self.userid
    def get_email(self):
        return self.email
    

    def list_action(self):
        msg = ''
        for key in self.action_dict:
            msg = msg + f'[{key}] {self.action_dict[key].get_name()}\n'
        return msg
    
    
    def read_action_from_client(self, conn):
        recv_msg = conn.recv(100).decode("utf-8")
        print(f'Receive msg from {client_addr}: {recv_msg}')
        while recv_msg not in action_dict:
            msg = "Wrong input, please select "
            for key in action_dict.keys():
                msg = msg + f'[{key}] '
            msg += ': '
            conn.send(msg.encode('utf-8'))
            # conn.send(f'Wrong input, please select "1", "2", or "3"\n---> '.encode('utf-8'))
            recv_msg = conn.recv(100).decode("utf-8")
        print("Do action:", recv_msg)
        
        return welcome_action_dict[recv_msg]