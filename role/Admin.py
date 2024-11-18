from .User import User

from action.classroom_management.ManageClassroom import ManageClassroom
from action.course_management.ManageCourse import ManageCourse
from action.ListUserInfo import ListUserInfo
from action.event.SearchEvent import SearchEvent

class Admin(User):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)
        self.user_action =  super().get_available_action() + [
                                ManageClassroom("Add/Remove/Modify/Search Classroom"),
                                ManageCourse("Add/Upload/Remove/Modify/Search Course"),
                                ListUserInfo("List User Information"),
                                SearchEvent("Search Study Event")
                            ]
        

    def isAdmin(self):
        return True