import asyncio
from ipaddress import IPv4Network, IPv4Address
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM, SOCK_UDP, IPPROTO_TCP, IPPROTO_UDP

class Base:
    def to_json(self):
        pass

    def __repr__(self):
        items = [f'{k}={v}' for k, v in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(items)[:-2]})>"

class Scanner:
    def __init__(self, network):
        self.network = IPv4Network(network)
        self.ports = [ 20, 21, 22, 23, 25, 80, 111, 135, 136, 137, 138, 139, 443, 445, 631, 993, 995 ]
        self.results = type('Scan', Base, {})
        
    async def scan_range(self, r):
        for a in self.network.hosts():
            tasks.append(asyncio.create_task(scan_addr(a, p, pro, f)))
        asyncio.gather(tasks)

    async def scan_addr(self, addr, port, proto, flags):
        for port in ports:
            s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP))
            r = s.connect_ex((a, p))
            
        if r == 0:
            d = s.recv(1024)
            print(f'{a} returned {d} on {p}')
        elif r == 11:
            print(f'{a} on {p} is timeout')
        else:
            print(f'{a} on {p} is closed')

if __name__ == '__main__':
    s = Scanner(argv[1])
    asyncio.run(s.scan_range())
