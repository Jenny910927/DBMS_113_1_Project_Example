from ..Action import Action
from utils import list_option, get_selection
from .AddCourse import AddCourse
from .UploadCourses import UploadCourses
from .RemoveCourse import RemoveCourse
from .ModifyCourse import ModifyCourse
# from .SearchCourse import SearchCourse
class ManageCourse(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [
                        AddCourse("Add Course"),
                        UploadCourses("Upload Course csv file"),
                        RemoveCourse("Remove Course"), 
                        ModifyCourse("Modify Course"), 
                        # SearchCourse("Search Course")
                        ]

    def exec(self, conn, user):
        print("Manage Course")

        
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))
        
    

        action = get_selection(conn, self.options)
        action.exec(conn)

        
        # conn.send(f'\nUpdate successfully! New {item}: {new_value}\n'.encode('utf-8'))
        