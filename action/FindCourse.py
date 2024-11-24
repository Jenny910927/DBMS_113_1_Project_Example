from .Action import Action
from DB_utils import find_course
class FindCourse(Action):
    def exec(self, conn, user):
        print("Find Course")
        conn.send(" (enter None if don't want to search based on the item)\n".encode('utf-8'))
        instructor_name = self.read_input(conn, "instructor name")
        course_name = self.read_input(conn, "course name")
        print(f'Find Course | {instructor_name}, {course_name}')
        
        table = find_course(instructor_name, course_name)
        self.send_table(conn, table)
    
        return 