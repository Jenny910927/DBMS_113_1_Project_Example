from .Action import Action
from DB_utils import list_available_study_group
class ListEvent(Action):
     def exec(self, conn, user):
        print("List Event")
        list_available_study_group()
        
        # TODO