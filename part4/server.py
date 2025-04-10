from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Rediriger / vers /templates/index.html
        if self.path == '/':
            self.path = '/templates/index.html'
        
        # Gérer les chemins pour les fichiers statiques
        if self.path.startswith('/static/'):
            self.path = self.path[1:]  # Enlever le premier slash
        elif self.path.startswith('/templates/'):
            self.path = self.path[1:]  # Enlever le premier slash
            
        return SimpleHTTPRequestHandler.do_GET(self)

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    # Changer le répertoire de travail vers le dossier du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serveur démarré sur http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrêté")
        httpd.server_close()

if __name__ == '__main__':
    run() 