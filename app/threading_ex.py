#!/usr/bin/python3

from threading import Thread
from time import sleep

class MyThread(Thread):
    def __init__(self, name, count, wait):
        super().__init__()
        self.name = name
        self.count = count
        self.wait = wait
        self.exited = False

    def run(self):
        while self.count > 0:
            print(f'Hello from {self.name}')
            sleep(self.wait)
            self.count -= 1
        self.exited = True

threads = []
        
for i in range(1,5+1):
    threads.append(MyThread(name=f'Thread{i}', count=i, wait=i*.5))
    threads[i-1].start()

for t in threads:
    t.join()

print(f'MainThread exit')
