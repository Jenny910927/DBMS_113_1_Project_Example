from ..Action import Action
from DB_utils import course_exist, update_course
from utils import list_option, get_selection

class ModifyCourse(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["Course_name", "Instructor_name", "Department_name", "Lecture_time"]


    def exec(self, conn):
        course_id = self.read_input(conn, "course id")

        if not course_exist(course_id):
            conn.send(f'\nCourse does not exist!\n'.encode('utf-8'))
            return
        

        msg = '[INPUT]Which do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        select_item = get_selection(conn, self.options)

        
        new_value = self.read_input(conn, f'new value for {select_item}')

        update_course(course_id, select_item, new_value)


        conn.send(f'\nModify course successfully!\n'.encode('utf-8'))