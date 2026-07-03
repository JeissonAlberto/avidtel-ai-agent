import http.server, socketserver, os, json
class H(http.server.SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/s':
   self.send_response(200);self.send_header('Content-type','application/json');self.end_headers()
   self.wfile.write(json.dumps({"o":1245}).encode())
  else: return super().do_GET()
 def do_POST(self):
  if self.path=='/c':
   l=int(self.headers['Content-Length']);d=json.loads(self.rfile.read(l))
   m=d.get('message','').lower();r="Hola Jeisson, monitoreando Avidtel." if "hola" in m else "Activo."
   self.send_response(200);self.send_header('Content-type','application/json');self.end_headers()
   self.wfile.write(json.dumps({"r":r}).encode())
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("",80),H) as s: s.serve_forever()
