import socket
from chatlib import *# To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    send_server = build_message(code ,data)
    conn.send(send_server.encode())
    #print(send_server)


def recv_message_and_parse(conn):
    full_msg = conn.recv(102400).decode()
    cmd, data = parse_message(full_msg)
    return cmd, data


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    # Implement code
    print(error_msg)
    exit()


def login(conn):
    while True:
        username = input("Hey friend enter your username:")
        passward = input("Now enter your passward:")
        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], f"{username}#{passward}")
        if recv_message_and_parse(conn) == ("LOGIN_OK" ,""):
            break
        else:
            continue


def logout(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")

def main():
    login(connect())
    logout(connect())



if __name__ == '__main__':
    main()
