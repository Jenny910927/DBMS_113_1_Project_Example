from ..Action import Action
from DB_utils import classroom_exist, remove_classroom

class RemoveClassroom(Action):
    def exec(self, conn):
        classroom_id = self.read_input(conn, "classroom id")

        if not classroom_exist(classroom_id):
            conn.send(f'\nClassroom does not exist!\n'.encode('utf-8'))
            return

        remove_classroom(classroom_id)

        conn.send(f'\nRemove classroom successfully!\n'.encode('utf-8'))