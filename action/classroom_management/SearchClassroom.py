from ..Action import Action
from DB_utils import search_classroom

class SearchClassroom(Action):
    def exec(self, conn, user):

        conn.send(" (enter None if don't want to search based on item)\n".encode('utf-8'))
        building_name = self.read_input(conn, "building name")
        capacity_size = self.read_input(conn, "capacity size")
        floor_number = self.read_input(conn, "floor number")
        room_name = self.read_input(conn, "room name")
        print(f'Find Course | {building_name}, {capacity_size}, {floor_number}, {room_name}')
        
        table = search_classroom(building_name, capacity_size, floor_number, room_name)
        conn.send('\n'.encode('utf-8'))
        conn.send(table.encode('utf-8'))
        conn.send('\n'.encode('utf-8'))
    

        

        conn.send(f'\nRemove classroom successfully!\n'.encode('utf-8'))