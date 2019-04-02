from threading import Thread


class envir:
    def __init__(self):
        self.name = 'eee'

    def change_mac(self, other, name):
        self.name = 'd'
        other.my_mac =  name

class node:
    def __init__(self):
        self.my_mac = '1234'


def create_node (env_):
    i_am_node = node()
    env = env_
    
my_list = [] 
global_env = envir()
for i in range(0, 5):
    thread1 = Thread(target=create_node, args=(global_env, ))
    my_list.append(thread1)
    thread1.start()
    