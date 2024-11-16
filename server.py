import socket
from threading import Thread
from action.LogIn import LogIn
from action.SignUp import SignUp
from action.Exit import Exit
from action.Logout import Logout
from action.CreateEvent import CreateEvent
from action.ListEvent import ListEvent
from action.ListHistory import ListHistory
from action.JoinEvent import JoinEvent
from action.LeaveEvent import LeaveEvent
from action.ModifyUserInfo import ModifyUserInfo

from role.User import User

from DB_utils import *
from utils import *

welcome_action_dict = {
    '1': LogIn("Log-in"),
    '2': SignUp("Sign-up"),
    '3': Exit("Leave System")
}

user_action_dict = {
    '1': CreateEvent("Create Study Event"),
    '2': ListEvent("List All Available Study Events"),
    '3': JoinEvent("Join Study Event"),
    '4': LeaveEvent("Leave Study Event"),
    '5': ListHistory("List Study Group History"),
    '6': ModifyUserInfo("Modify User Info"),
    '7': Logout("Logout"),
    '8': Exit("Leave System")
}



def handle_connection(conn, client_addr):
    try:
        
        while True: # Welcome Page
            conn.send("----------------------------------------\nWelcome to Study Group System! Please select your option:\n".encode('utf-8'))
            conn.send(f'[INPUT]Please select your option:\n{list_option(welcome_action_dict)}---> '.encode('utf-8'))
            
            # conn.send(msg.encode('utf-8'))
                
            action = get_selection(conn, welcome_action_dict)
            
            user = action.exec(conn)
            if user == -1:
                raise Exception("End connection")
            
            send_msg =  f'\n----------------------------------------\n\nHi {user.get_username()}!\n' + \
                        f'[ User Info ] {user.get_info_msg_no_pwd()}\n'
            conn.send(send_msg.encode('utf-8'))

            while True: # Function Page
                
                # conn.send(f'----------------------------------------\nHi {user.get_username()}!\n'.encode('utf-8'))
                # conn.send(f'User Info | userid: {user.get_userid()}, username: {user.get_username()}, email: {user.get_email()}\n'.encode('utf-8'))
                conn.send(f'\n----------------------------------------\n\n'.encode('utf-8'))
                conn.send(f'[INPUT]Please select your option:\n{list_option(user_action_dict)}---> '.encode('utf-8'))
                action = get_selection(conn, user_action_dict)
                ret = action.exec(conn, user)
                if ret == -1:
                    break

            
            

    except Exception:
        print(f"Connection with {client_addr} close.")
        conn.close()
    finally:
        print(f"Connection with {client_addr} close.")
        conn.close()







if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    # fetch_data(cur, cmd="login")

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