class Action():    
    def __init__(self, action_name):
        self.action_name = action_name
    def exec(self, conn, **kwargs):
        raise NotImplementedError
    def get_name(self):
        return self.action_name
    
    def read_input(self, conn, name):
        ret = conn.send(f'[INPUT]Please enter {name}: '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
        return recv_msg