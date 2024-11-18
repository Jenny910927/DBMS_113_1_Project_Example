from ..Action import Action
from DB_utils import classroom_exist, update_classroom
from utils import list_option, get_selection

class ModifyClassroom(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["Building_name", "Floor_number", "Room_name", "Capacity_size"]

    def exec(self, conn):
        classroom_id = self.read_input(conn, "classroom id")

        if not classroom_exist(classroom_id):
            conn.send(f'\nClassroom does not exist!\n'.encode('utf-8'))
            return
        

        msg = '[INPUT]Which do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        select_item = get_selection(conn, self.options)

        
        new_value = self.read_input(conn, f'new value for {select_item}')

        update_classroom(classroom_id, select_item, new_value)


        conn.send(f'\nModify classroom successfully!\n'.encode('utf-8'))