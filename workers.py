import socket
import threading
from config import WORKERS

def run_worker(name, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"✔ Distributed [{name}] Worker Node active on port {port}")
    
    while True:
        conn, _ = server.accept()
        try:
            data = conn.recv(1024).decode()
            a, b = map(float, data.split(','))
            
            # Execute math operations directly inside dedicated backend loops
            if name == "ADD": res = a + b
            elif name == "SUB": res = a - b
            elif name == "MUL": res = a * b
            elif name == "DIV": res = a / b if b != 0 else "Error: Div by Zero"
            
            conn.send(str(round(res, 4) if isinstance(res, float) else res).encode())
        except Exception as e:
            conn.send(f"Worker Error: {str(e)}".encode())
        finally:
            conn.close()

if __name__ == "__main__":
    print("=== Booting Distributed Computing Worker Grid ===")
    threads = []
    for name, (host, port) in WORKERS.items():
        t = threading.Thread(target=run_worker, args=(name, host, port), daemon=True)
        t.start()
        threads.append(t)
        
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down Worker Grid.")
