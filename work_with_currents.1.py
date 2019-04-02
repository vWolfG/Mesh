#coding: UTF-8
import threading
import time

class envir:
    def __init__(self):
        self.my_dict = [None] * 4
    
    
    def change_list(self, i, j):
        self.my_dict[i] = j 


def for_thread(envi,i,j):
    lock.acquire()
    try: 
        envi.change_list(i,j)
    finally:
        lock.release()
    

env = envir()
lock = threading.RLock()
threads = []
for i in range(0,4): 
    thread1 = threading.Thread(target=for_thread, args=( env,i,'first'))
    thread1.start()
    threads.append(thread1)
    time.sleep(0.5)
    print(env.my_dict[i])  
    thread2 = threading.Thread(target=for_thread, args=( env,i, 'second' ))
    thread2.start()
    threads.append(thread2)
    time.sleep(0.5)
    print(env.my_dict[i])

for i in threads:
    i.join()