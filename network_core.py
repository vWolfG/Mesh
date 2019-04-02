import igraph as ig
import json
import threading
import time

len_len = 2  # change it, it is length place for len_data, no more than 99
MAC_len = 17 
type_len = 1 

def draw_graph(graph_dict):
        vertices = []
        edges = []
        for i in range(0,len(graph_dict)):
                vertices.append(str(i))
        
        for key in graph_dict:
                for val in graph_dict[key]:
                        tuple_ = (int(key),int(val))
                        revers_tuple = tuple_[::-1]
                        if revers_tuple not in edges:
                                edges.append(tuple_)
        g = ig.Graph(vertex_attrs={"label": vertices}, edges=edges, directed=False)
        visual_style = {}
        
        #  Scale vertices based on degree
        indegree = g.indegree()
        visual_style["vertex_size"] = [x/max(indegree)*50+110 for x in indegree]

        #layout = g.layout("kk")
        ig.plot(g) 
        return len(edges)

class Environment:

    def __init__(self,file_name):
        self.lock = threading.RLock()
        self.config = open(file_name)
        self.node_inform = []
        self.global_graph = dict()
        # creating list with number of nodes and their macAddr
        # the first element is number of nodes
        for line in self.config:
            str_1 = ''.join(line.split()).split(':')
        
            if str_1[0] == "Connections":
                break

            if str_1[1] not in self.node_inform:
                self.node_inform.append(str_1[1])
            else: 
                raise Exception('Similar Mac addresses')
                
        # creating global connection graph between nodes key = node, value = list of neighbourhood

        for line in self.config: 
            str_2 = line.strip().split('-')
            
            if str_2[0] in self.global_graph:
                self.global_graph[str_2[0]].append(str_2[1])
            else:
                self.global_graph[str_2[0]] = list(str_2[1])
        
            if str_2[1] in self.global_graph:
                self.global_graph[str_2[1]].append(str_2[0])
            else:
                self.global_graph[str_2[1]] = list(str_2[0])

        # checking for validation
        if int(self.node_inform[0]) != (len(self.node_inform) - 1):
            raise Exception('Configuration file is not corrected. Mismatch amount of nodes.')

        # creating list of connection number 0-len of nodes with their Mac_addr
        self.Mac_to_index = self.node_inform[1:]
        self.config.close()

        self.amount_edges = draw_graph(self.global_graph)
        self.rbuffer_list = [None] * int(self.node_inform[0])

    
    
    
    # sending message to all neighbourhoods with using global network graph
    def send_to_neighbourhood(self, mes, from_who, i):
        self.lock.acquire()                             # block global variable
        try:
            for j in self.global_graph[str(i)]:
                self.rbuffer_list[int(j)] = mes
        finally:
            self.lock.release()
    
    def clean_rbuff(self,i):
        self.lock.acquire()                             # block global variable
        try:
            self.rbuffer_list[i] = None 
        finally:
            self.lock.release()
             
    
    #def creating_dict(my_dict, node_list):
        

class Packet:
    
    def __init__(self, mac_ad):
        self.received_packet = None
        self.my_MAC = mac_ad

        self.node_graph = {}
        self.node_graph[self.my_MAC] = list() # table with roads between nodes

    def create_packet(self, type_p, other, data, my_mac_addr):
        my_str =  str(type_p) + str(len(data) + len(other.MAC_address)*2) + str(other.MAC_address) + str(my_mac_addr) + str(data) # reconstruct this, it is temporary 
        return my_str
    
    def new_received_packet(self, received_packet):
        self.received_packet = received_packet

    @staticmethod 
    def packet_for_me_or(mac_addr, message):
            if mac_addr == ''.join(message):
                return True
            else:
                return False

    def graph_packet(self):
        return '3'+ str(self.my_MAC) + json.dumps(self.node_graph)

    
    def update_graph(self, neig_dict, new_neigh):
        if new_neigh not in self.node_graph[self.my_MAC]:
            self.node_graph[self.my_MAC].append(new_neigh)
        for key, val in neig_dict.items():
            if key in self.node_graph:
                for i in val:
                    if i not in self.node_graph[key]:
                        self.node_graph[key].append(i)           
            else:
                self.node_graph[key] = val

    def pars_packet(self,mac_addr):
        # type 2 = send direct data
        # type 3 = route table
        # type 4 = send data to remote node
        word = list(''.join(self.received_packet.split()))
        r_message = str()
        if word[0] == '2' and Packet.packet_for_me_or(mac_addr, word[3:20]) == True:  # word[1:2] - length of pocket,  word[3:20] -  (mac_len = 17 )Mac_address destination
            data_len = 21 + int(''.join(word[1:3]))
            return ''.join(word[20:data_len])
        if word[0] == '3': 
            neigh_mac = ''.join(word[1:18])
            neigh_dict = json.loads(''.join(word[18:]))
            self.update_graph(neigh_dict, neigh_mac)
            return "initialization from " + ''.join(word[1:18]) + "  I am " + str(mac_addr) + "\n"
        #if word[0] == '4'and Packet.packet_for_me_or(mac_addr, word[3:20]) == True: 
        return r_message
        # self.packet_type
        

class Node:
    def __init__(self, MAC_addr):
        self.MAC_address = MAC_addr
        self.My_Pack = Packet(MAC_addr) 
        
        
        

    def __str__(self):
        return ("{}").format(self.MAC_address)   

    def send_packet(self, type_p, other, data):
        self.my_file = open ("log_mesh.txt","a+") 
        message = "Send packet from "+ str(self.MAC_address) + " to " + str(other.MAC_address) + " Data: " + str(data) +"\n"
        self.my_file.write(message)
        self.my_file.close() 
        sending_packet = self.My_Pack.create_packet(type_p, other, data, self.MAC_address)#del
        other.My_Pack.new_received_packet(sending_packet) # del
       # return self.My_Pack.create_packet(type_p, other, data, self.MAC_address)
    
    def get_packet(self):
        if not self.My_Pack.received_packet:
            pass
        else: 
            message = self.My_Pack.pars_packet(self.MAC_address)
            if message[0:4] == "init":
                self.my_file = open ("log_mesh.txt","a+")
                self.my_file.write(str(message))
                self.my_file.close()
            else:
                if message != False:
                    self.my_file = open ("log_mesh.txt","a+")
                    str1 = "Received packet by "+ str(self.MAC_address) + " from " + str(message[0:MAC_len]) + " Data: " + str(message[MAC_len:]) +"\n"
                    self.my_file.write(str1)
                    self.my_file.close() 
            self.My_Pack.received_packet = None
    
    def initialisation(self, other):
        other.node_graph