from .Action import Action
from DB_utils import list_user_info
class ListUserInfo(Action):
     def exec(self, conn, user):
        print("List User Info")

        userid = self.read_input(conn, "user id that you want to show")

        table = list_user_info(userid)
        conn.send('\n'.encode('utf-8'))
        conn.send(table.encode('utf-8'))
        conn.send('\n'.encode('utf-8'))
    
        return 