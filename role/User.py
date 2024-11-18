from .Role import Role

class User(Role):
    def __init__(self, userid, username, pwd, email, isUser, isAdmin):
        self.userid = userid
        self.username = username
        self.pwd = pwd
        self.email = email
        self.isUser = isUser
        self.isAdmin = isAdmin
        
        self.role = 'Admin' if isAdmin else 'User'
        print(f'Create user | userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}, role: {self.role}')

    def get_info_msg_no_pwd(self):
        return f'userid: {self.userid}, username: {self.username}, email: {self.email}, role: {self.role}'
    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}, role: {self.role}'
    def get_username(self):
        return self.username
    def get_userid(self):
        return self.userid
    def get_email(self):
        return self.email
    def check_isAdmin(self):
        return self.isAdmin
    

    def list_action(self):
        msg = ''
        for key in self.action_dict:
            msg = msg + f'[{key}] {self.action_dict[key].get_name()}\n'
        return msg
    
    