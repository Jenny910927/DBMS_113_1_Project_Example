from .Action import Action
class Exit(Action):
    def exec(self, conn):
        conn.send(f'[EXIT]Exit system. Bye~'.encode('utf-8'))
        return -1

    