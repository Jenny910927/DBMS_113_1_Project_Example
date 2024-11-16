from .Action import Action
from DB_utils import list_history
class ListHistory(Action):
     def exec(self, conn, user):
         print("List Hostory")
         table = list_history(user.get_userid())
         conn.send('\n'.encode('utf-8'))
         conn.send(table.encode('utf-8'))
         conn.send('\n'.encode('utf-8'))
        
         return 