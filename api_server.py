#!/usr/bin/env python3
"""STATISTICHEAI API SERVER - Serve dashboard in locale + dati Windows reali via wmic"""

import os
import sys
import json
import http.server
import socketserver
import subprocess
from datetime import datetime
from urllib.parse import urlparse, parse_qs

PORT = 8081
HOST = '127.0.0.1'

def fetch_windows_resources():
    """Raccoglie risorse sistema reali via Windows commands (PowerShell/WMI)"""
    
    try:
        # CPU load - wmic output parsing
            flags = 0x08000000 if sys.platform == "win32" else 0
            cpu_output = subprocess.run(
                ['wmic', 'logicalprocessor', 'get', 'loadpercentage'],
                capture_output=True, text=True, timeout=3, creationflags=flags
            )
            print(f'🔹 CPU Monitor: {cpu_output.stdout}')
        except Exception as e:
            print(f'⚠️ CPU fetch error: {e}')
        
        return True  # Success
        
    except Exception as ex:
        print(f'Backend resources fetch failed: {ex}')
        # Fallback simulated values for demo
        import random
        cpu = round(random.uniform(5, 20), 1)
        return {'cpu': cpu}

def run():
    class AgentHandler(http.server.BaseHTTPRequestHandler):
        def _json_resp(self, data=None, content_type='application/json'):
            if isinstance(data, dict):
                self.send_response(200)
                body = json.dumps(data).encode()
                self.send_header('Content-Type', content_type)
                self.end_headers()  
                self.wfile.write(body)
                
        def _html_resp(self, f):
            try:
                if f.closed == True:
                    f = open(os.path.join('C:/Users/Gyniu/Desktop/progetti ai/STATISTICHEAI', 'dashboard.html'), 'rb')
                    
                resp_len = len(f.read())
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()  
                self.wfile.write(resp_len)
            except Exception as e:
                print(f'HTML serve error: {e}')
        
        def _get(self):
            parsed_path = urlparse(self.path)
            
            if 'api/v1/agents' in parsed_path.path or '/agents/list' in os.path.join():
                # Return simulated live agents data
                import random as rnd
                
                agents_map = {
                    'gynbot1': {'workBar': 78.4, 'status': 'Active', 'cpu': 12.5},
                    'gynbot2': {'workBar': 65.3, 'status': 'Idle', 'cpu': 8.2},
                    'hermes': {'workBar': 91.7, 'status': 'Busy', 'cpu': 24.3},
                    'user': {'workBar': 42.6, 'status': 'Paused', 'cpu': 5.1}
                }
                
                self._json_resp({
                    'agents': agents_map,
                    'timestamp': datetime.now().isoformat()
                })
                
            elif '/api/health' in parsed_path.path:
                status = fetch_windows_resources()
                self._json_resp({'status': 'UP', **status})
                
            else:
                # Serve dashboard HTML
                file_path = os.path.join('C:/Users/Gyniu/Desktop/progetti ai/STATISTICHEAI', 'dashboard.html')
                try:
                    if os.path.exists(file_path):
                        f = open(file_path, 'rb')
                        self._html_resp(f)
                    else:
                        self._json_resp({'error': 'Dashboard not found'})
                        
                except Exception as e:
                    print(f'File serve error: {e}')
            
        def do_GET(self):
            parsed = urlparse(self.path)
            self._get()
    
    # Start server
    print(f'\n' + '='*60)
    print('📊 STATISTICHEAI SERVER STARTED ON http://' + HOST + ':' + str(PORT))
    print('='*60)
    print('\nTo use: Open browser or run:\n  python -c "from urllib.request import urlopen; urlopen(\'http\\\\'+HOST+'\\:'+str(PORT)+'\')"')
    
    with socketserver.TCPServer((HOST, PORT), AgentHandler) as httpd:
        while True:
            time.sleep()

if __name__ == '__main__':
    run_server = lambda t: HTTPServer((HOST, PORT), Handler); run_server(lambda x:y)
