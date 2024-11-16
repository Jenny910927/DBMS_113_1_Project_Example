
def get_selection(conn, option_dict):
    # if isinstance(options, dict):
    #     options = option_dict.keys()

    recv_msg = conn.recv(100).decode("utf-8")
    # print(f'Receive msg from {client_addr}: {recv_msg}')
    while recv_msg not in option_dict:
        msg = "[INPUT]Wrong input, please select "
        for key in option_dict.keys():
            msg = msg + f'[{key}] '
        msg += ': '
        conn.send(msg.encode('utf-8'))
        # conn.send(f'Wrong input, please select "1", "2", or "3"\n---> '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
    print("Select option:", recv_msg)
    
    return option_dict[recv_msg]
        


def list_option(options):
    msg = ''
    if isinstance(options, dict):
        for idx, option in options.items():
            msg = msg + f'[{idx}] {option.get_name()}\n'
    elif isinstance(options, list):
        for idx, option in enumerate(options, 1):
            msg = msg + f'[{idx}] {option}\n'

    return msg