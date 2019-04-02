import network_core as network

def do_init(env,node,i):
    for k in range(0, int(env.node_inform[0])*env.amount_edges):
        env.send_to_neighbourhood(node.My_Pack.graph_packet(),node.MAC_address, i) 
        network.time.sleep(0.5)
        for j in range(0,int(env.node_inform[0])):
            my_mess =  envir.rbuffer_list[i]
            if my_mess != None:
                envir.clean_rbuff(i)
                node.My_Pack.received_packet = my_mess
                node.get_packet()





#creating environment for network
envir = network.Environment('conf.txt')
nodes = []
threads = []
#creating nodes
for i in range(1,int(envir.node_inform[0])+1):
    node = network.Node(envir.node_inform[i])
    nodes.append(node)

# cycle of creating threads
for i in range(0, int(envir.node_inform[0])):
    thread = network.threading.Thread(target=do_init, args=(envir,nodes[i],i))
    thread.start()
    threads.append(thread)
    network.time.sleep(0.5)

#start threads
for i in threads:
    i.join()

print("hello!")
# do sending config
# example "0->1 hello!", send from node 0 to node 1 the message "hello!"
# conf_file = open("sending_config.txt")
# for line in conf_file:
#     letters = line.split()
#     if len(letters) != 2:
#         raise Exception('Syntax Error sending_config file')
#     nodes_send = letters[0].split('->')
#     if len(nodes_send) != 2:
#         raise Exception('Syntax Error sending_config file, nodes')
#     data = letters[1]
#     for i in nodes_send:
#         if int(i) >= int(envir.node_inform[0]):
#             raise Exception('There is no such node')
        
#     nodes[int(nodes_send[0])].send_packet(2,nodes[int(nodes_send[1])], data)
    
#     nodes[int(nodes_send[1])].get_packet()