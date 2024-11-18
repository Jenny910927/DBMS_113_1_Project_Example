from ..Action import Action
from DB_utils import course_exist, remove_course

class RemoveCourse(Action):
    def exec(self, conn):
        course_id = self.read_input(conn, "course id")

        if not course_exist(course_id):
            conn.send(f'\nCourse does not exist!\n'.encode('utf-8'))
            return

        remove_course(course_id)

        conn.send(f'\nRemove course successfully!\n'.encode('utf-8'))