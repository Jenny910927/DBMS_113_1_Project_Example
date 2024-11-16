from .Action import Action
from DB_utils import leave_study_group
class LeaveEvent(Action):
     def exec(self, conn, user):
        print("Leave Event")
        
        event_id = self.read_input(conn, "study event id")
      #   join_time = self.read_input(conn, "join time (in YYYY-MM-DD HH-MI-SS format)")

        leave_study_group(user.get_userid(), event_id)

        conn.send(f'\nLeave study group successfully!\n'.encode('utf-8'))
        