from .Action import Action
class Exit(Action):
    def exec(self, conn, user=None):
        conn.send(f'[EXIT]Exit system. Bye~\n'.encode('utf-8'))
        return -1

    