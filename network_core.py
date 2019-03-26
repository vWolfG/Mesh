import igraph as ig

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

class Environment:

    def __init__(self,file_name):
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
        draw_graph(self.global_graph)

    


class Packet:
    
    def __init__(self):
        self.received_packet = None

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


    def pars_packet(self,mac_addr):
        # type 2 = send direct data
        # type 3 = route table
        # type 4 = send data to remote node
        word = list(''.join(self.received_packet.split()))
        r_message = str()
        if word[0] == '2' and Packet.packet_for_me_or(mac_addr, word[3:20]) == True:  # word[1:2] - length of pocket,  word[3:20] -  (mac_len = 17 )Mac_address destination
            data_len = 21 + int(''.join(word[1:3]))
            return ''.join(word[20:data_len])
        #if word[0] == '3'and Packet.packet_for_me_or(mac_addr, word[3:20]) == True: 
        #if word[0] == '4'and Packet.packet_for_me_or(mac_addr, word[3:20]) == True: 
        return r_message
        # self.packet_type
        

class Node:
    def __init__(self, MAC_addr):
        self.MAC_address = MAC_addr
        self.R_buffer = Packet() # receiver
        self.T_buffer = Packet()   # transmitter buffer
       # self.network_table = Network() # table with roads between nodes
    def __str__(self):
        return ("{}").format(self.MAC_address)   

    def send_packet(self, type_p, other, data):
        self.my_file = open ("log_mesh.txt","a+") 
        message = "Send packet from "+ str(self.MAC_address) + " to " + str(other.MAC_address) + " Data: " + str(data) +"\n"
        self.my_file.write(message)
        self.my_file.close() 
        sending_packet = self.T_buffer.create_packet(type_p, other, data, self.MAC_address)
        other.R_buffer.new_received_packet(sending_packet)

    def get_packet(self):
        if not self.R_buffer.received_packet:
            pass
        else: 
            message = self.R_buffer.pars_packet(self.MAC_address)
            if message != False:
                self.my_file = open ("log_mesh.txt","a+")
                str1 = "Received packet by "+ str(self.MAC_address) + " from " + str(message[0:MAC_len]) + " Data: " + str(message[MAC_len:]) +"\n"
                self.my_file.write(str1)
                self.my_file.close() 
            self.R_buffer.received_packet = None