from .Action import Action
from DB_utils import list_available_study_group
class JoinEvent(Action):
     def exec(self, conn, user):
        print("Join Event")
        
        event_id = self.read_input(conn, "study event id")
        
        
        # TODO