from socket import socket, setdefaulttimeout, AF_INET, SOCK_STREAM
from ipaddress import IPv4Network, IPv4Address

import threading
from threading import Thread, activeCount

from time import sleep

class Scanner:
    def __init__(self, network):
        self.Network = network
        self.Ports = [ 20, 21, 22, 23, 25, 80, 111, 135, 137, 138, 139, 443, 445, 631, 993, 995 ]
        self._threads = []
        
    @property
    def Network(self):
        return self._network

    @Network.setter
    def Network(self, o):
        try:
            self._network = IPv4Network(o)
        except ValueError as e:
            raise e

    @property
    def Ports(self):
        return self._ports
    
    @Ports.setter
    def Ports(self, o):
            # these should be try/except
        assert(type(o) is list), f'{o} should be list'
        assert(type(i) is int for i in o), f'{i} in {o} is not int'
        self._ports = o

    @property
    def Threads(self):
        return len(self._threads)

    def check_network(self, o):
        try:
            m = IPv4Network(o)
            for i in self.Network.subnets(abs(self.Network.prefixlen-m.prefixlen)):
                if i == m:
                    return True
        except Exception:
                # we don't care what was entered if it wasn't a network
            return False

    def scan_network(self):
        results = []

        for i in self.Network.hosts():
            t = ScanHost(host=i.compressed, ports=self.Ports)
            t.start()
                # this sucks and needs to get fixed?
            if activeCount() > 500:
                while activeCount() > 500:
                    pass
            self._threads.append(t)

        for t in self._threads:
            t.join()

        for t in self._threads:
            results.append(t.Results)
        return results

    def scan_host(self, host):
        results = []

        for p in self.Ports:
            if threading.activeCount() < self.MAX_THREADS:
                self._threads.append(Scan(host=host, port=p))

        for t in self._threads:
            t.start()

        for t in self._threads:
            t.join()

        for t in self._threads:
            results.append(t.Results)
        return results

class ScanHost(Thread):
    def __init__(self, host, ports):
        super().__init__()
        self.host = host
        self.ports = ports
        self.threads = []
        self.Results = {
            'host':self.host,
            'ports':[]
        }

    def run(self):
        for p in self.ports:
            t = Scan(self.host, p)
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        for t in self.threads:
            self.Results['ports'].append(t.Results)

class Scan(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.Results = {
            'port':self.port,
            'status':''
        }
    
    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(1)
        r = sock.connect_ex( (self.host, self.port) )
        if r == 0:
            self.Results['status'] = 'OPEN'
        elif r == 11:
            self.Results['status'] = 'TIMEOUT'
        else:
            self.Results['status'] = 'CLOSED'
        sock.close()
