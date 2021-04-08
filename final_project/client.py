import socket
from chatlib import *# To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def build_and_send_message(conn, code, data):
    send_server = build_message(code ,data)
    conn.send(send_server.encode())
    #print(send_server)


def recv_message_and_parse(conn):
    full_msg = conn.recv(1024000000).decode()
    cmd, data = parse_message(full_msg)
    return cmd, data


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
            print("Welcome dear freind of mine.\nAre you ready for a game ?")
            break
        else:
            print("A mistake crept in\nplease try again.")
            continue

def build_send_recv_parse(conn ,code ,data=""):
    """:return the server's answer splited to code and data."""
    build_and_send_message(conn, code ,data)
    msg_cod, recv_data = recv_message_and_parse(conn)
    #print(msg_cod, recv_data)
    return msg_cod ,recv_data

def get_score(conn):
    msg_cod, recv_data = build_send_recv_parse(conn ,"MY_SCORE")
    if msg_cod == "YOUR_SCORE":
        print(f"{msg_cod}{recv_data}")
    else:
        print(f"Eror\n{msg_cod, recv_data}")


def get_highscore(conn):
    msg_cod, recv_data = build_send_recv_parse(conn, "HIGHSCORE")
    if msg_cod == "ALL_SCORE":
        print(msg_cod, recv_data)
    else:
        print(f"Eror\n{msg_cod, recv_data}")


def play_question(conn):
    msg_cod, recv_data = build_send_recv_parse(conn, "GET_QUESTION")
    if msg_cod == "YOUR_QUESTION":
        print(msg_cod)
        a = 0
        for i in range(-1,5):
            if a <= 1 :
                print(recv_data.split('#')[a])
                a += 1
            else:
                print(f"{i}. {recv_data.split('#')[a]} \n")
                a += 1
        id = recv_data.split("#")[0]
        answer = (input("Set your aswer her :")).strip()
        cmd, correct_or_wrong = build_send_recv_parse(conn, "SEND_ANSWER", join_data([id, answer]))
        if cmd == "CORRECT_ANSWER":
            print("Well done !!")
        elif cmd == "WRONG_ANSWER":
            print(f"You filed . \nThe correct answer is{correct_or_wrong}")
    elif msg_cod == "NO_QUESTIONS":
        print("Hey man we run out from questions.")
        return
    else:
        print(f"Eror\n{msg_cod, recv_data}")
        return

def get_logged_users(conn):
    msg_cod, recv_data = build_send_recv_parse(conn, "LOGGED")
    print(msg_cod, recv_data)


def logout(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")


def main():
    con = connect()
    login(con)
    while True:
        chose = (input("Chosse: \ns to see your score :) \na to see all scores ^_^"
                       "\nq to get a question \nl to logout :(\n ")).strip()
        if chose == "s":
            get_score(con)
        elif chose == "a":
            get_highscore(con)
        elif chose == "q":
            play_question(con)
        elif chose == "l":
            print("BYE :)")
            logout(con)
            break




if __name__ == '__main__':
    main()
