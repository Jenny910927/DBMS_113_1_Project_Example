from .Action import Action
from DB_utils import join_study_group
class JoinEvent(Action):
     def exec(self, conn, user):
        print("Join Event")
        
        event_id = self.read_input(conn, "study event id")
        join_time = self.read_input(conn, "join time (in YYYY-MM-DD HH-MI-SS format)")

        join_study_group(user.get_userid(), event_id, join_time)

        conn.send(f'\nJoin study group successfully!\n'.encode('utf-8'))
        