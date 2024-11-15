from .Action import Action
class UserAuthenticate(Action):
    
    def exec(self, conn):
        raise NotImplementedError
        
    
    def read_userinfo(self, conn, info_str):
        ret = conn.send(f'[INPUT]Please enter {info_str}: '.encode('utf-8'))
        if ret == -1:
            print(f'sening error')
        recv_msg = conn.recv(100).decode("utf-8")
        # print(f'Receive userinfo: {info_str}={recv_msg}')
        return recv_msg


    # def read_userid(self, conn):
    #     # print(f'Enter read_userid')
    #     conn.send(f'[ {self.action_name} ]\nPlease enter userid: '.encode('utf-8'))
    #     recv_msg = conn.recv(100).decode("utf-8")
    #     # print(f'Receive userinfo: {recv_msg}')
    #     return recv_msg

    # def read_pwd(self, conn, confirm_pwd=False):
    #     # print(f'Enter read_pwd')
    #     if confirm_pwd:
    #         conn.send("Please confirm your password: ".encode('utf-8'))
    #     else:
    #         conn.send("Please enter password: ".encode('utf-8'))
    #     recv_msg = conn.recv(100).decode("utf-8")
    #     # print(f'Receive userinfo: {recv_msg}')
    #     return recv_msg
    
    
    # def _userid_exist(self, userid): # TODO
    #     return True
    
   
    
    