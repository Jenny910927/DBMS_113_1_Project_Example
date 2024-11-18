import socket
from os.path import isfile, getsize


conn_ip = "127.0.0.1"
conn_port = 8800

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
client_socket.connect((conn_ip, conn_port))

try: 
    while True: # Keep receiving and sending message with server
        
        recv_msg = client_socket.recv(10000).decode('utf-8')
        if not recv_msg:
            print("Connection closed by the server.")
            break
        if recv_msg.find("[EXIT]") != -1:
            print(recv_msg.replace("[EXIT]", ''), end='')
            break
        if recv_msg.find("[CSV]") != -1:
            print(recv_msg.replace("[CSV]", '').replace("[INPUT]", ''), end='')
            
            filename = input().strip()
            if not isfile(filename) or filename.find(".csv") == -1:
                print(f'File \'{filename}\' is not found or is not a csv file.')
                client_socket.send("[NOTFOUND]".encode('utf-8'))
            

            
            file_size = getsize(filename)
            # print(f'File \'{filename}\' found, file_size = {file_size}')
            client_socket.send(str(file_size).encode())
        
            # Wait for server response
            client_socket.recv(1024)
            print(f'Start transferring file...')

            with open(filename, 'rb') as f:
                while (chunk := f.read(1024)):
                    client_socket.send(chunk)
            print(f'File \'{filename}\' sent successfully.')
        
        elif recv_msg.find("[INPUT]") != -1:
            print(recv_msg.replace("[INPUT]", ''), end='')

            send_msg = input().strip()
            while len(send_msg) == 0:
                print("Input cannot be empty. Please enter again:", end=' ')
                send_msg = input().strip()

            if send_msg == "exit":
                break            
            client_socket.send(send_msg.encode('utf-8'))
        

        else:
            print(recv_msg, end='')
        
finally:
    print("Connection close.")
    client_socket.close()