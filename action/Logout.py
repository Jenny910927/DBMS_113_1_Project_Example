from .Action import Action
class Logout(Action):
    def exec(self, conn, user=None):
        conn.send(f'<Logout>\n\n'.encode('utf-8'))
        return -1

    