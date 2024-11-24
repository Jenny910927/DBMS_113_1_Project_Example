from ..Action import Action
from DB_utils import list_available_study_group
class ListEvent(Action):
    def exec(self, conn, user):
        print("List Event")

        conn.send("Please wait for fetching data...\n".encode('utf-8'))

        table = list_available_study_group()

        self.send_table(conn, table)
        
        return