from .Action import Action
from DB_utils import list_history
class ListHistory(Action):
     def exec(self, conn, user):
         print("List Hostory")
         table = list_history(user.get_userid())
         self.send_table(conn, table)
        
         return 