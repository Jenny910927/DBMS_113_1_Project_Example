class UserAuthenticate:
    def __init__(self, action_name):
        self.action_name = action_name

    def read_username(self, conn):
        raise NotImplementedError

    def read_pwd(self, conn):
        raise NotImplementedError
    
    
    def _userid_exist(): # TODO
        return True
    
    def _correct_pwd(): # TODO
        return True