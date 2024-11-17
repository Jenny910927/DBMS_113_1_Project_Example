from ..Action import Action
from utils import list_option, get_selection
from .AddClassroom import AddClassroom
from .RemoveClassroom import RemoveClassroom
class ManageClassroom(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [AddClassroom("Add Classroom"),
                        RemoveClassroom("Remove Classroom"), 
                        # "Modify Classroom", "SearchClassroom"
                        ]

    def exec(self, conn, user):
        print("Manage Course")

        
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))
        
    

        action = get_selection(conn, self.options)
        action.exec(conn, user)

        
        # conn.send(f'\nUpdate successfully! New {item}: {new_value}\n'.encode('utf-8'))
        