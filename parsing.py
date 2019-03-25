conf_file = open("sending_config.txt")
for line in conf_file:
    letters = line.split()
    if len(letters) != 2:
        raise Exception('Syntax Error sending_config file')
    nodes = letters[0].split('->')
    if len(nodes) != 2:
        raise Exception('Syntax Error sending_config file, nodes')
    data = letters[1]
    
