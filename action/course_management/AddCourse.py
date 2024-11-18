from ..Action import Action
from DB_utils import append_course, course_exist

class AddCourse(Action):
    def exec(self, conn):
        course_name = self.read_input(conn, "course_name")
        instructor_name = self.read_input(conn, "main instructor name")
        department_name = self.read_input(conn, "department name")
        lecture_time = self.read_input(conn, "lecture time")

        course_id = append_course(course_name, instructor_name, department_name, lecture_time)

        conn.send(f'\nAppend course successfully! New Course_id: {course_id}\n'.encode('utf-8'))