from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.event.CreateEvent import CreateEvent
from action.event.ListEvent import ListEvent
from action.event.JoinEvent import JoinEvent
from action.event.LeaveEvent import LeaveEvent
from action.ListHistory import ListHistory
from action.FindCourse import FindCourse
from action.FindReserved import FindReserved
from action.ModifyUserInfo import ModifyUserInfo


class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action =  [
                                CreateEvent("Create Study Event"),
                                ListEvent("List All Available Study Events"),
                                JoinEvent("Join Study Event"),
                                LeaveEvent("Leave Study Event"),
                                ListHistory("List Study Group History"),
                                FindCourse("Find Course"),
                                FindReserved("Find Reserved Classroom"),
                                ModifyUserInfo("Modify User Information"),
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
        

