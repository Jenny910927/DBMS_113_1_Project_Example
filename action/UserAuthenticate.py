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


    
   
    
    