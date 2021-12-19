class Node:

    connectedTo = []
    def __init__(self, key, name, url=None,description=None,public_metrics=None, isPrimary = False, associated_Keyword = None):
        self.connectedTo = []
        self.id = key
        self.name = name
        self.url = url
        self.description = description
        self.public_metrics = public_metrics
        self.isPrimary = isPrimary
        self.associated_Keyword = associated_Keyword

    def setConnectedTo(self, connectionsList):
        self.connectedTo = connectionsList

    def addNeighbor(self,id_neighbor):
        self.connectedTo.append(id_neighbor)

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def getConnections(self):
        return self.connectedTo

    def getId(self):
        return self.id

    def __str__(self):
        return str(self.id) + 'is connected to' + str((x.id, x.weight) for x in self.connectedTo)

    def getUsername(self):
        return self.name
    
    def equals(self, other):
        if not isinstance(other, Node):
            return False
        elif self.id == other.id:
            return True
        else:
            return False
