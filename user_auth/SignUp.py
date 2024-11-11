from .UserAuthenticate import UserAuthenticate
class SignUp(UserAuthenticate):
    def read_userid(self, conn):
        conn.send("[ Log-in ]\nPlease enter userid: ".encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
        return recv_msg
    def read_pwd(self, conn):
        conn.send("[ Log-in ]\nPlease enter password: ".encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
        return recv_msg
        
    def _userid_exist():
        return False
    