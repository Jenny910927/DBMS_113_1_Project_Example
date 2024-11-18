from ..Action import Action
from DB_utils import append_classroom

class AddClassroom(Action):
    def exec(self, conn):
        building_name = self.read_input(conn, "building name for new classroom")
        capacity_size = self.read_input(conn, "capacity size")
        floor_number = self.read_input(conn, "floor number")
        room_name = self.read_input(conn, "room name")

        classroom_id = append_classroom(building_name, capacity_size, floor_number, room_name)

        conn.send(f'\nCreate new classroom successfully! New Classroom_id: {classroom_id}\n'.encode('utf-8'))