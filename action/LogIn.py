from .UserAuthenticate import UserAuthenticate
from DB_utils import fetch_user
class LogIn(UserAuthenticate):
    def exec(self, conn):
        userid = self.read_userinfo(conn, "userid")
        print(f'Read userid: {userid}')

        username, pwd, email, role = fetch_user(userid)
        print(f'After fetch')

        # while not self._userid_exist(userid):
        while username is None:
            conn.send("Userid not exist, please enter userid: ".encode('utf-8'))
            userid = self.read_userinfo(conn, "userid")

        pwd_input = self.read_userinfo(conn, "password")
        print(f'Read pwd: {pwd_input}')
        count = 2
        # while count > 0 and not self._correct_pwd(pwd_input, pwd):
        while count > 0 and pwd_input != pwd:
            conn.send(f'Password incorrect, please enter password (remaining try: {count}): '.encode('utf-8'))
            # pwd = self.read_pwd(conn)
            pwd_input = conn.recv(100).decode("utf-8")
            count -= 1
        if count == 0:
            conn.send(f'Password incorrect'.encode('utf-8'))
            raise Exception("Wrong Password")


    # def _correct_pwd(self, pwd_input, pwd_correct): # TODO
    #     return True

      
    