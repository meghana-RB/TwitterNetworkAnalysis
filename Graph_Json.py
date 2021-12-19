import json
import networkx as nx
import Graph

def graph_to_json(graph):
    dict_of_nodes = {}
    for node in graph.nodes():
        dict_of_nodes[node.getId()] = [node.name, node.url, node.description, node.public_metrics, node.isPrimary, node.associated_Keyword, node.connectedTo]
    with open('Twitter_Graph.json', 'w') as f:
        json.dump(dict_of_nodes, f)

def load_graph_from_json(filename):
    graph = nx.Graph()
    labels = {}
    with open(filename, 'r') as f:
        graph_data = json.load(f)
#Graph.Node(followers['id'], followers['username'], followers['url'], followers['description'], followers['public_metrics'], isPrimary=False)
    for item in graph_data.items():
        item
        node = Graph.Node(key = item[0], name = item[1][0], url = item[1][1], description = item[1][2], public_metrics = item[1][3], isPrimary = item[1][4], associated_Keyword = item[1][5])
        node.setConnectedTo(item[1][6])
        graph.add_node(node)
        if node.isPrimary:
            labels[node] = node.associated_Keyword + "\n(" + node.getUsername() + ")"
        else:
            labels[node] = node.getUsername()
        for node in graph.nodes():
            for neighbor in node.getConnections():
                for otherNode in graph.nodes():
                    if neighbor == otherNode.getId():
                        graph.add_edge(node, otherNode)

    return graph,labels