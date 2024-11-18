from ..Action import Action
from DB_utils import create_study_group
class CreateEvent(Action):
    
    def exec(self, conn, user):
        print("Create Event")
        course_id = self.read_input(conn, "course id")
        classroom_id = self.read_input(conn, "classroom id")
        content = self.read_input(conn, "study description")
        user_max = self.read_input(conn, "maximum number of user")
        event_date = self.read_input(conn, "event date (in YYYY-MM-DD format)")
        event_period_start = self.read_input(conn, "event start time (between 8 to 21)")
        event_duration = self.read_input(conn, "event duration (min=1, max=3)")


        

        user_id = user.get_userid()
        print("User id =", user_id)
        

        event_id = create_study_group(content, user_max, course_id, user_id, 
                            event_date, event_period_start, event_duration, classroom_id)
        
        if event_id == -1:
            conn.send(f'\nCreate study group fail :(  This time is not available.\n'.encode('utf-8'))
        else:
            conn.send(f'\nCreate study group successfully! Event id: {event_id}\n'.encode('utf-8'))
            

