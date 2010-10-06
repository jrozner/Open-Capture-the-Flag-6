#!/usr/bin/python3

import socketserver
import binascii
import subprocess

port = 12345
intro = """\n\nWelcome to Dr. Mario's Crypto Clinic! What is the patient's name?\n\n>"""
badname = "How the hell are you supposed to pronounce that? That name's not on my list.\n"
reply = "\nHmm... I think we got your name right.\nIs your name spelled like this? (y/n):  "
fail1 = "\nWoah buddy, what're you trying to pull? GTFO before we call the feds!\n"
fail2 = "Well then you should learn how to spell before you come back!\n"
patients = ['bowser', 'luigi', 'mario', 'peach', 'toad', 'waluigi', 'wario', 'yoshi']

class Appointment(socketserver.StreamRequestHandler):
    
    def sanitize(self, infection):
        sanitary = []
        vaccine = ''
        i = 0
        while i < len(infection):
            j = hex(infection[-i-1]^0x45).split("x")[1]
            sanitary.append(j)
            i += 1
        for each in sanitary:
            if 19 < int(each,16):
                vaccine += binascii.unhexlify(each).decode()
        return vaccine

    def gen_Rx(self, patient):
        appointment = False
        for each in patients:
            if each == patient.split(';')[0]:
                appointment = True
        if appointment:
            rX = "/home/drmario/appts/" + patient
            unsafe = subprocess.Popen('/home/drmario/appts/appt',
                                      shell=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            result = unsafe.communicate(rX.encode())[0]
            self.wfile.write(result + '\n'.encode())
        else:
            self.wfile.write(badname.encode())
        return
    
    def handle(self):
        self.wfile.write(intro.encode())
        raw_stuff = self.rfile.readline().strip()
        sanitized = self.sanitize(raw_stuff)
        self.wfile.write((reply + sanitized + "\n\n>").encode())
        raw_reply = self.rfile.readline().decode().strip()
        if (raw_reply == 'n'):
            self.wfile.write(fail2.encode())
        elif(raw_reply == 'y'):
            self.gen_Rx(sanitized)
        else:
            self.wfile.write(fail1.encode())
        return
       
class Clinic(socketserver.ThreadingTCPServer):
    daemon_threads = True
    pass

def main():
    easy_doc = Clinic(('', port), Appointment)
    easy_doc.serve_forever()

if __name__ == "__main__":
    main()
