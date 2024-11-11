import socket


conn_ip = "127.0.0.1"
conn_port = 8800

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
client_socket.connect((conn_ip, conn_port))

while True:
    recv_msg = client_socket.recv(100)
    print(recv_msg.decode('utf-8'), end='')
    send_msg = input()
    client_socket.send(send_msg.encode('utf-8'))
    
    # Client end connection
    if send_msg == "exit":
        break



print("Connection close.")
client_socket.close()