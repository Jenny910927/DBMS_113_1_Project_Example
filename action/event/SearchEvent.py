from ..Action import Action
from DB_utils import search_study_event
class SearchEvent(Action):
    def exec(self, conn, user):
        print("Search Event")
        
        course_name = self.read_input(conn, "course name")
        
        table = search_study_event(course_name)
        self.send_table(conn, table)
        
        return


