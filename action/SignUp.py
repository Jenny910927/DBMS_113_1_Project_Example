from .UserAuthenticate import UserAuthenticate
from role.User import User
from DB_utils import db_register_user, username_exist

class SignUp(UserAuthenticate):
    def exec(self, conn):
        # print(f'Enter SignUp Action')

        # Read Username
        username = self.read_userinfo(conn, "username")
        while username_exist(username):
            # conn.send("[INPUT]Username exist, please enter another username: ".encode('utf-8'))
            conn.send("Username exist, ".encode('utf-8'))
            username = self.read_userinfo(conn, "another username")
        
        # Read Password
        pwd = self.read_userinfo(conn, "password")
        # TODO: double check pwd
        # pwd2 = self.read_pwd(conn, confirm_pwd=True)
        # if(pwd != pwd2):


        # Read_email
        email = self.read_userinfo(conn, "email")

        # Add to DB
        userid = db_register_user(username, pwd, email)
        conn.send(f'----------------------------------------\nSuccessfully create account! Userid = {userid}\n'.encode('utf-8'))

        return User(userid, username, pwd, email, True, False)



    
    # def _username_exist(self, username):
    #     # TODO
    #     return False
    