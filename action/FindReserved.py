from .Action import Action
from DB_utils import find_reserved_room_on_date
class FindReserved(Action):
    def exec(self, conn, user):
        print("Find Reserved")

        event_date = self.read_input(conn, "event date (in YYYY-MM-DD format)")
        
        table = find_reserved_room_on_date(event_date)

        self.send_table(conn, table)

        return 