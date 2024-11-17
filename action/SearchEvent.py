from .Action import Action
from DB_utils import search_study_event
class SearchEvent(Action):
    def exec(self, conn, user):
        print("Search Event")
        
        course_name = self.read_input(conn, "course name")
        
        table = search_study_event(course_name)

        conn.send('\n'.encode('utf-8'))
        conn.send(table.encode('utf-8'))
        conn.send('\n'.encode('utf-8'))
        return


