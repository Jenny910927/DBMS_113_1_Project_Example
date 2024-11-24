
from .Action import Action
from role.User import User
from role.Admin import Admin
from DB_utils import fetch_user

class LogIn(Action):
    def exec(self, conn):
        userid = self.read_input(conn, "userid")
        print(f'Read userid: {userid}')

        while not userid.isdigit():
            conn.send("Input is not numeric, ".encode('utf-8'))
            userid = self.read_input(conn, "correct userid")


        username, pwd, email, isUser, isAdmin = fetch_user(userid)
        print(f'--After fetch')

        while username is None:
            conn.send("Userid not exist, ".encode('utf-8'))
            userid = self.read_input(conn, "correct userid")
            username, pwd, email, isUser, isAdmin = fetch_user(userid)

        pwd_input = self.read_input(conn, "password")
        print(f'Read pwd: {pwd_input}')
        count = 2
        
        while count > 0 and pwd_input != pwd:
            conn.send(f'[INPUT]Password incorrect, please enter password (remaining try: {count}): '.encode('utf-8'))
            pwd_input = conn.recv(100).decode("utf-8")
            count -= 1
        if count == 0:
            conn.send(f'[EXIT]Connection close. Reason: Password incorrect.'.encode('utf-8'))
            return -1
        
        if isAdmin:
            return Admin(userid, username, pwd, email)
            
        else:
            return User(userid, username, pwd, email)
    