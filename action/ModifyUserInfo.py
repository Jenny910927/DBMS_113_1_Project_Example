from .Action import Action
from DB_utils import userid_exist, update_user_info
from utils import list_option
class ModifyUserInfo(Action):
     
    def __init__(self, action_name):
        super().__init__(action_name)
        self.info_option = ["User_name", "Password", "Email"]

    def exec(self, conn, user):
        print("Modify User Info")

        userid = user.get_userid()

        if user.isAdmin(): # Admin can modify any user's info
            userid = self.read_input(conn, "userid that you want to change")

            while not userid.isdigit():
                conn.send("Input is not numeric, ".encode('utf-8'))
                userid = self.read_userinfo(conn, "correct userid")
            
            if not userid_exist(userid):
                conn.send("Userid not exist.\n".encode('utf-8'))
                return

        
        msg = '[INPUT]Which do you want to modify?\n' + list_option(self.info_option) + '---> '
        conn.send(msg.encode('utf-8'))

        recv_msg = conn.recv(100).decode("utf-8")
        item = self.info_option[int(recv_msg)-1]
        print(f'Select option: {recv_msg} -> {item}')
        new_value = self.read_input(conn, f'new value for {item}')


        update_user_info(userid, item, new_value)
        conn.send(f'\nUpdate successfully! New {item}: {new_value}\n'.encode('utf-8'))
        