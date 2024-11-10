import socket
from threading import Thread



def handle_connection(conn, client_addr):
    while True:
        try:
            conn.send("Hi, this is server.".encode('utf-8'))
            recv_msg = conn.recv(100)
            if len(recv_msg) == 0:
                break 
            print(f'Receive msg from {client_addr}: {recv_msg.decode("utf-8")}')
            
        except Exception:
            break
    
    print(f"Connection with {client_addr} close.")
    conn.close() # close connection with the client




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