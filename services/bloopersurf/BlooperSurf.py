#!/usr/bin/env python3

import socketserver
from socket import *
import random
import threading
import select
import time


port = 8888
kiddie_pool = []
intro = """
Welcome to Crazy 8s Blooper Surfing, here's your Blooper!
Ride around to collect all 8 Red Coins.
Better be quick though, they don't hang around for long....
First Red Coin appeared at:  """
alert = "Checkpoint reached! Next Red Coin appeared at:  "
almost = "You're almost there! Head to the finish line:  "
finish = "Goooooooool! Here's your prize! ::\n\n\t"

class Blooper(threading.Thread):
    head = """.....0/0000\\0.....
....0/000000\\0....
...00/000000\\00...
..00/00000000\\00..
.000/00000000\\000.
000/0000000000\\000
.../00"""
    tail = """000\...
...000000000000...
...0==========0...
...=00======00=...
...0==0====0==0...
...0==0====0==0...
..0=00======00=0..
..00//000000\\\\00..
../000000000000\..
..00.00000000.00..
../0./00..00\.0\..
..00.00....00.00..
../0./0....0\.0\..
...0.00....00.0...
...0./0....0\.0...
...0..0....0..0...
......0....0......\n"""
    
    def __init__(self, client_addy):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ckpts = 0
        self.racing = True
        self.tentacle = client_addy
        self.racer = str(oct(int(client_addy.strip().split(".")[:3][0])))
        self.bloop = self.head + self.racer + self.tail
        self.ports = []
        for port in range(9):
            self.ports.append(random.randint(51000, 61000))

    def run(self):
        while self.racing:
            if (self.ckpts < 8):
                self.racing = self.chkpt()
                self.ckpts += 1
            else:
                self.gol()
                self.ckpts += 1
                self.racing = False    
        return

    def chkpt(self):
        addy = ('', self.ports[self.ckpts])
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(addy)
        sock.listen(1)
        try:
            r2r, r2w, ie = select.select([sock], [], [], 3)
            if sock in r2r:
                coin, player1 = sock.accept()
                squiddy = coin.recv(1024)
                if (squiddy.decode().strip() == self.bloop.strip()):
                    if (self.ckpts == 7):
                        carryon = almost + str(oct(self.ports[(self.ckpts + 1)])).split("o")[1] + "\n"
                    else:
                        carryon = alert + str(oct(self.ports[(self.ckpts + 1)])).split("o")[1] + "\n"
                    coin.send(carryon.encode())
                    coin.close()
                    sock.close()
                    return True
                else:
                    coin.send("\nInvalid Blooper\n\n".encode())
                    print("Bad Blooper from " + self.tentacle + "\n" + squiddy.decode().strip())
                    coin.close()
                    sock.close()
                    return False
            else:
                print(time.ctime().split(" ")[3] + " " + self.tentacle + " made it through " + str(self.ckpts) + " coins.")
                sock.close()
                return False
        except Exception as inst:
            print("Oh oh- " + str(inst))
            sock.close()
            return False

    def gol(self):
        prize = finish + open("flag.txt", mode='r').read(-1) + "\n"
        addy = ('', self.ports[self.ckpts])
        goal = socket(AF_INET, SOCK_STREAM)
        goal.bind(addy)
        goal.listen(1)
        try:
            r2r, r2w, ie = select.select([goal], [], [], 3)
            if goal in r2r:
                winrar, player2 = goal.accept()
                finished = winrar.recv(1024)
                if (finished.decode().strip() == self.bloop.strip()):
                    winrar.send(prize.encode())
                    print(time.ctime().split(" ")[3] + " " + self.tentacle + " - Victory confirmed.")
                else:
                    print(time.ctime().split(" ")[3] + " " + self.tentacle + " lost it in the end...")
                winrar.close()
                goal.close()    
                return
        except Exception as inst:
            print(inst)
            goal.close()
            return

class TentalceRape(socketserver.StreamRequestHandler):
    def handle(self):
        racerX = Blooper(self.client_address[0])
        portocall = str(oct(racerX.ports[0])).split("o")[1]
        print(time.ctime().split(" ")[3] + " " + self.client_address[0]  + ' - Connected')
        burp = intro + portocall + "\n\n" + racerX.bloop 
        self.wfile.write(burp.encode())
        racerX.start()
        kiddie_pool.append(racerX)
        return

class BlooperServ(socketserver.ThreadingTCPServer):
    daemon_threads = True
    pass

def main():
    GooperBlooper = BlooperServ(('', port), TentalceRape)
    GooperBlooper.serve_forever()

if __name__ == "__main__":
    main()
