import socket


conn_ip = "127.0.0.1"
conn_port = 8800

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
client_socket.connect((conn_ip, conn_port))

while True:
    recv_msg = client_socket.recv(100)
    print("Receive msg from server:", recv_msg.decode('utf-8'))
    send_msg = input("Please input msg: ")
    
    client_socket.send(send_msg.encode('utf-8'))
    
    # Client end connection
    if send_msg == "exit":
        break




client_socket.close()