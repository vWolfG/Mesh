import network_core as network

   

envir = network.Environment('conf.txt')
nodes = []
for i in range(1,int(envir.node_inform[0])+1):
    nodes.append(network.Node(envir.node_inform[i]))  # nodes creating 
    # print(nodes[i-1])



# example "0->1 hello!", send from node 0 to node 1 the message "hello!"
conf_file = open("sending_config.txt")
for line in conf_file:
    letters = line.split()
    if len(letters) != 2:
        raise Exception('Syntax Error sending_config file')
    nodes_send = letters[0].split('->')
    if len(nodes_send) != 2:
        raise Exception('Syntax Error sending_config file, nodes')
    data = letters[1]
    for i in nodes_send:
        if int(i) >= int(envir.node_inform[0]):
            raise Exception('There is no such node')
        
    nodes[int(nodes_send[0])].send_packet(2,nodes[int(nodes_send[1])], data)
    print(nodes[int(nodes_send[1])].get_packet())