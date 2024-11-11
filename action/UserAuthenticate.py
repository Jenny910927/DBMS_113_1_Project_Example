from .Action import Action
class UserAuthenticate(Action):
    def exec(self, conn): # TODO
        # pass
        userid = self.read_userid(conn)
        pwd = self.read_pwd(conn)
        print(f'Receive userid = {userid}, pwd = {pwd}')
    
    def read_userid(self, conn):
        raise NotImplementedError

    def read_pwd(self, conn):
        raise NotImplementedError
    
    
    def _userid_exist(self): # TODO
        return True
    
    def _correct_pwd(self): # TODO
        return True
    
    