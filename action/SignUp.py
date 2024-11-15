from DB_utils import db_register_user
from .UserAuthenticate import UserAuthenticate
class SignUp(UserAuthenticate):
    def exec(self, conn):
        print(f'Enter SignUp Action')
        # Read Userid
        userid = self.read_userinfo(conn, "userid")
        while self._userid_exist(userid):
            conn.send("Userid exist, please enter another userid: ".encode('utf-8'))
            userid = self.read_userinfo(conn, "userid")

        # Read Userid
        username = self.read_userinfo(conn, "username")       
        
        # Read Password
        pwd = self.read_userinfo(conn, "password")
        # TODO: double check pwd
        # pwd2 = self.read_pwd(conn, confirm_pwd=True)
        # if(pwd != pwd2):


        # Read_email
        email = self.read_userinfo(conn, "email")

        # Add to DB
        db_register_user(userid, username, pwd, email)

        # return userid, username, pwd, email, "User"

        pass


    
    def _userid_exist(self, userid):
        return False
    