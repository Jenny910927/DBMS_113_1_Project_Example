from ..Action import Action
from DB_utils import isInEvent, leave_study_group
class LeaveEvent(Action):
    def exec(self, conn, user):
        print("Leave Event")
        
        event_id = self.read_input(conn, "study event id")


        if not isInEvent(user.get_userid(), event_id):
            conn.send(f'\nYou are not in this event!\n'.encode('utf-8'))
            return
        
        leave_study_group(user.get_userid(), event_id)

        conn.send(f'\nLeave study group successfully!\n'.encode('utf-8'))

