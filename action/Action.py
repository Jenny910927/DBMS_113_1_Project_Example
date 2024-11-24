class Action():    
    def __init__(self, action_name):
        self.action_name = action_name
    def exec(self, conn, **kwargs):
        raise NotImplementedError
    def get_name(self):
        return self.action_name
    
    def read_input(self, conn, show_str):
        ret = conn.send(f'[INPUT]Please enter {show_str}: '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
        return recv_msg
    
    def send_table(self, conn, table): 
        # Since the table is too long, buffer size is not enough for client to receive the whole message.
        # Add a [END] tag to mark the end of the message
        conn.sendall(("[TABLE]" + '\n' + table + '\n' + "[END]").encode('utf-8'))

        