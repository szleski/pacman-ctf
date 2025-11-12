#!/usr/bin/env python3
"""
Lightweight web server for viewing Pacman CTF replay files.
Converts replay files to JSON and serves a web-based viewer.
"""

import pickle
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class ReplayHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/viewer.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.startswith('/api/replays'):
            self.send_replay_list()
        elif self.path.startswith('/api/replay/'):
            replay_file = self.path.split('/')[-1]
            self.send_replay_data(replay_file)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def send_replay_list(self):
        """Send list of available replay files"""
        replay_files = [f for f in os.listdir('.') if f.startswith('replay-')]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(replay_files).encode())
    
    def send_replay_data(self, replay_file):
        """Convert replay pickle to JSON and send"""
        try:
            with open(replay_file, 'rb') as f:
                replay_data = pickle.load(f)
            
            # Convert to JSON-serializable format
            json_data = {
                'layout': {
                    'width': replay_data['layout'].width,
                    'height': replay_data['layout'].height,
                    'walls': [[replay_data['layout'].walls[x][y] for y in range(replay_data['layout'].height)] 
                              for x in range(replay_data['layout'].width)],
                    'food': [[replay_data['layout'].food[x][y] for y in range(replay_data['layout'].height)] 
                             for x in range(replay_data['layout'].width)],
                    'capsules': replay_data['layout'].capsules,
                },
                'actions': [(idx, str(action)) for idx, action in replay_data['actions']],
                'length': replay_data['length'],
                'redTeamName': replay_data.get('redTeamName', 'Red'),
                'blueTeamName': replay_data.get('blueTeamName', 'Blue'),
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(json_data).encode())
        except Exception as e:
            self.send_error(500, f"Error loading replay: {str(e)}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ReplayHandler)
    print(f"Replay viewer server running on http://localhost:{port}")
    print(f"Open your browser and go to http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
