import socket
from threading import Thread
from user_auth.LogIn import LogIn
from user_auth.SignUp import SignUp



def handle_connection(conn, client_addr):
    while True:
        try:
            # User Welcome 
            conn.send(f'Welcome to Study Group System! Please select your option:\n[1] Log-in\t[2] Sign-up\n---> '.encode('utf-8'))
            recv_msg = conn.recv(100).decode("utf-8")
            # if len(recv_msg) == 0:
            #     break 

            print(f'Receive msg from {client_addr}: {recv_msg}')

            
            while recv_msg != '1' and recv_msg != '2':
                 conn.send(f'Wrong input, please select "1" or "2"\n---> '.encode('utf-8'))
                 recv_msg = conn.recv(100).decode("utf-8")
                 print(f'Receive msg from {client_addr}: {recv_msg}')
            
            if recv_msg == '1': 
                action = LogIn("Log-in")
            else: # Sign-up
                action = SignUp("Sign-up")
            
            userid = action.read_userid(conn)
            pwd = action.read_pwd(conn)
            print(f'Receive userid = {userid}, pwd = {pwd}')


            



        except Exception:
            break
    
    print(f"Connection with {client_addr} close.")
    conn.close() # close connection with the client


if __name__ == '__main__':


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

    server_socket.close()