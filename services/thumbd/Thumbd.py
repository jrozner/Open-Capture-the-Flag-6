#!/usr/bin/env python3

import socketserver
import subprocess

port = 2222
level = "./thumbd"

class Pipe(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write("Enter a username:\t".encode())
        argstring = self.rfile.readline().strip()
        e = subprocess.Popen(level, shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout_val = e.communicate(argstring)[0]
        self.wfile.write(stdout_val)

class Warp(socketserver.ThreadingTCPServer):
    daemon_threads = True
    pass

def main():
    wz = Warp(('', port), Pipe)
    wz.serve_forever()

if __name__ == "__main__":
    main()
