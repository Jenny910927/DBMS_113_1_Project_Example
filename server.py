import socket
from threading import Thread
from action.LogIn import LogIn
from action.SignUp import SignUp
from action.Exit import Exit
from action.CreateEvent import CreateEvent
from action.ListEvent import ListEvent
from action.ModifyUserInfo import ModifyUserInfo

from role.User import User

from DB_utils import *


welcome_action_dict = {
    '1': LogIn("Log-in"),
    '2': SignUp("Sign-up"),
    '3': Exit("Leave System")
}

user_action_dict = {
    '1': CreateEvent("Create Study Event"),
    '2': ListEvent("List All Available Study Events"),
    # '3': JoinEvent("Join Study Event"),
    '4': ModifyUserInfo("Modify User Info"),
    # '5': Logout("Logout"),
    '6': Exit("Leave System")
}

def get_action(action_dict):
    recv_msg = conn.recv(100).decode("utf-8")
    print(f'Receive msg from {client_addr}: {recv_msg}')
    while recv_msg not in action_dict:
        msg = "Wrong input, please select "
        for key in action_dict.keys():
            msg = msg + f'[{key}] '
        msg += ': '
        conn.send(msg.encode('utf-8'))
        # conn.send(f'Wrong input, please select "1", "2", or "3"\n---> '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
    print("Do action:", recv_msg)
    
    return action_dict[recv_msg]
        


def list_action(action_dict):
    msg = ''
    for key in action_dict:
        msg = msg + f'[{key}] {action_dict[key].get_name()}\n'
    return msg



def handle_connection(conn, client_addr):
    try:
        print("Enter handle connection")
        msg = "Welcome to Study Group System! Please select your option:\n" + list_action(welcome_action_dict) + "---> "
        print(msg)
        conn.send(msg.encode('utf-8'))
            
        action = get_action(welcome_action_dict)
        
        user = action.exec(conn)
        if user == -1:
            raise Exception("End connection")
        
        

        while True:
        
            # User Welcome 
            # conn.send(f'Welcome to Study Group System! Please select your option:\n[1] Log-in\t[2] Sign-up\t[3] Quit\n---> '.encode('utf-8'))
            
            
            conn.send(f'Hi {user.get_username()}! Please select your option:\n{user.list_action()}---> '.encode('utf-8'))
            action = get_action(user_action_dict)
            action.exec(conn)

            
            

    except Exception:
        print(f"Connection with {client_addr} close.")
        conn.close()
    finally:
        print(f"Connection with {client_addr} close.")
        conn.close()







if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    # fetch_data(cur, cmd="test")

    bind_ip = "127.0.0.1"
    bind_port = 8800

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)

    print(f'Server listening on {bind_ip}:{bind_port} ...')



    try:
        while True:
            (conn, client_addr) = server_socket.accept()
            print("Connect to client:", client_addr)

            thread = Thread(target=handle_connection, args=(conn, client_addr,))
            thread.start()
    finally:
        db.close()
        server_socket.close()