from .Action import Action
from DB_utils import list_available_study_group
class ListEvent(Action):
     def exec(self, conn, user):
         print("List Event")
         table = list_available_study_group()
         conn.send('\n'.encode('utf-8'))
         conn.send(table.encode('utf-8'))
         conn.send('\n'.encode('utf-8'))
        
         return 