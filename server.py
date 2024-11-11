import socket
from threading import Thread
from action.LogIn import LogIn
from action.SignUp import SignUp
from action.Exit import Exit

from DB_utils import *

welcome_action = {
    '1': LogIn("Log-in"),
    '2': SignUp("Sign-up"),
    '3': Exit("Exit")
}


def get_action(action_dict):
    recv_msg = conn.recv(100).decode("utf-8")
    print(f'Receive msg from {client_addr}: {recv_msg}')
    while recv_msg not in action_dict:
        msg = "Wrong input, please select "
        for key in action_dict.keys():
            msg = msg + f"{key}"
        conn.send(msg.encode('utf-8'))
        # conn.send(f'Wrong input, please select "1", "2", or "3"\n---> '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
    
    return welcome_action[recv_msg]
        
    

def handle_connection(conn, client_addr):
    while True:
        try:
            # User Welcome 
            conn.send(f'Welcome to Study Group System! Please select your option:\n[1] Log-in\t[2] Sign-up\t[3] Quit\n---> '.encode('utf-8'))
            
            # if len(recv_msg) == 0:
            #     break 

            action = get_action(welcome_action)
            action.exec(conn)
            
            
            # userid = action.read_userid(conn)
            # pwd = action.read_pwd(conn)
            # print(f'Receive userid = {userid}, pwd = {pwd}')

        except Exception:
            break
    
    print(f"Connection with {client_addr} close.")
    conn.close() # close connection with the client





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



    while True:
        (conn, client_addr) = server_socket.accept()
        print("Connect to client:", client_addr)

        thread = Thread(target=handle_connection, args=(conn, client_addr,))
        thread.start()   

    db.close()
    server_socket.close()