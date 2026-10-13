import socket
from config import COORDINATOR
print("=== DC - Distributed Calculator ===")
while True:
    print("\n1.ADD 2.SUB 3.MUL 4.DIV 5.EXIT")
    ch = input("Choice: ")
    if ch == "5": break
    op_map = {"1":"ADD","2":"SUB","3":"MUL","4":"DIV"}
    op = op_map.get(ch)
    if not op:
        print("Wrong choice")
        continue
    a = input("Enter a: ")
    b = input("Enter b: ")
    c = socket.socket()
    c.connect(COORDINATOR)
    c.send(f"{op},{a},{b}".encode())
    print(c.recv(1024).decode())
    c.close()