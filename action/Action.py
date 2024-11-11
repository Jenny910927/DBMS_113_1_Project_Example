class Action():    
    def __init__(self, action_name):
        self.action_name = action_name
    def exec(self, conn):
        raise NotImplementedError