#!/usr/bin/env python3

import socketserver
import random
import string
import re
import time

port = 1666
fail = "Oh well, not like you ever had a chance.  Good-bye!\n"
stxt = "Checking now... grab hold of your belts plumbers.\n\n"
won = "What's the only thing Mario wants to jump on? ::\n\n\t"
taunt = """\n\nWelcome to the Cipher Block Speed Run. Hope Mario can find a key pretty fast
'case I sure don't have it... Ready for the drop???\n\n"""
slow = "...\nWhat are you, a slowpoke?  Wrong video game, hustle up next time!\n\n"

def genTexts():
    mfile = "msgs/in" + str(random.randint(1, 6))
    btxt = open(mfile, mode='r').read(-1)
    return btxt

def genKeys():
    chrs = string.ascii_letters + string.digits
    randy = ''
    
    while ((len(randy)) < 8):
        randy += str(random.choice(chrs))
    return randy

def pToOTF(pwrd):
    key = 0
    
    for i in range(len(pwrd)):
        key += ord(pwrd[i])
        i += 1
    return key
    
def cryptoGen(btxt, otp):
    ciphertext = ''
    
    for indexer in range(len(btxt)):
        base = ord(btxt[indexer]) + otp
        temp1 = int(base / 3) + random.randint(-10, 10)
        temp2 = int(base / 3) + random.randint(-10, 10)
        temp3 = base - temp1 - temp2
        ciphertext += '.' + str(temp1) + '.' + str(temp2) + '.' + str(temp3)
    return ciphertext

def cryptoChk(ptxt, btxt, submission):
    keytry = pToOTF(submission)
    ptxt = re.sub('\D', ' ', ptxt)
    ptxt = ptxt.split()
    decrypted = ''
    index = 0
    counter = 0
    subTotal = 0
    
    while index < len(ptxt):
        while (counter < 3):
            subTotal += int(ptxt[index])
            index += 1
            counter += 1
        try:
            decrypted += chr(subTotal - keytry)
            subTotal = 0
            counter = 0
        except:
            return False
        
    if(decrypted == btxt):
        return True
    else:
        return False

class ShakeNBake(socketserver.StreamRequestHandler):
    def handle(self):
        newPass = genKeys()
        otp = pToOTF(newPass)
        btxt = genTexts()
        connection = self.client_address[0] + " " + time.ctime().split(" ")[3] + "\t"
        print('Connection from ' + connection + newPass + ":" + str(otp))
        cipherDump = cryptoGen(btxt, otp)
        self.wfile.write(taunt.encode())
        time.sleep(2)
        self.wfile.write("\t3\n".encode())
        time.sleep(1)
        self.wfile.write("\t2\n".encode())
        time.sleep(1)
        self.wfile.write("\t1\n".encode())
        time.sleep(1)
        self.wfile.write("\tGO!\n".encode())
        start = time.time()
        self.wfile.write(cipherDump.encode() + "\n\nKey plox? : ".encode())
        sub = self.rfile.readline().decode().strip()
        done = time.time()
        
        if ((done - start) > 10):
            self.wfile.write(slow.encode())
            return
        else:
            self.wfile.write(stxt.encode())
            data = cryptoChk(cipherDump, btxt, sub)
            time.sleep(2)
            if data:
                right = self.client_address[0] + " " + time.ctime().split(" ")[3] + "\t"
                right += sub + ":" + str(pToOTF(sub))
                print("Correct key from " + right)
                uwin = won + open("flag.txt", mode='r').read(-1) + "\n"
                self.wfile.write(uwin.encode())
            else:
                self.wfile.write(fail.encode())

class CryptoBot(socketserver.ThreadingTCPServer):
    daemon_threads = True
    pass

def main():
    CryptoBlooper = CryptoBot(('', port), ShakeNBake)
    CryptoBlooper.serve_forever()
    
if __name__ == "__main__":
    main()