from ..Action import Action
from datetime import datetime
from DB_utils import join_study_group
class JoinEvent(Action):
    def exec(self, conn, user):
        print("Join Event")
            
        event_id = self.read_input(conn, "study event id")
        

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        

        join_study_group(user.get_userid(), event_id, current_time)

        conn.send(f'\nJoin study group successfully!\n'.encode('utf-8'))
