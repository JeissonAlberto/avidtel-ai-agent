import http.server, socketserver, os, threading, time
PORT = 18800
DIRECTORY = "frontend"
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=DIRECTORY, **kwargs)
def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"--- AI AGENT DASHBOARD ---\nURL: http://localhost:{PORT}\nBy Jeisson Alberto")
        httpd.serve_forever()
if __name__ == "__main__":
    if not os.path.exists(DIRECTORY): os.makedirs(DIRECTORY)
    threading.Thread(target=start_server, daemon=True).start()
    try:
        while True: time.sleep(1)
    except: print("\nApagando...")
