from .Action import Action
class Exit(Action):
    def exec(self, conn):
        conn.send(f'Exit system. Bye~'.encode('utf-8'))
        pass

    