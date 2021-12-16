from GraphInterface import GraphInterface
from EdgeData import EdgeData
from NodeData import NodeData


class DiGraph(GraphInterface):
    def __init__(self):
        self._edgeOut = {}
        self._edgeIn = {}
        self._nodes = {}
        self._nodes_size = 0
        self._edge_size = 0
        self._mc = 0

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self._nodes and id1 in self._nodes:
            return self._edgeIn[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self._nodes and id1 in self._nodes:
            return self._edgeOut[id1]

    def get_all_v(self) -> dict:
        if self._nodes:
            return self._nodes

    def v_size(self) -> int:
        return len(self._nodes)

    def e_size(self) -> int:
        return self._edge_size

    def get_mc(self) -> int:
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 != id2 and id1 in self._nodes and id2 in self._nodes and id2 not in self._edgeOut[id1] and weight > 0:
            self._edgeOut[id1][id2] = EdgeData(id1, id2, weight)
            self._edgeIn[id2][id1] = id1
            self._edge_size = self._edge_size + 1
            self._mc = self._mc + 1
            return True
        return False

    def get_node(self, node_id: int) -> NodeData:
        if node_id in self._nodes:
            return self._nodes.get(node_id)

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes:
            return False
        node = NodeData(node_id)
        node.set_pos(pos[0], pos[1], pos[2])
        self._nodes[node_id] = node
        self._edgeOut[node_id] = {}
        self._edgeIn[node_id] = {}
        self._nodes_size = self._nodes_size + 1
        self._mc = self._mc + 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id in self._nodes:
            for vert_out in list(self.all_out_edges_of_node(node_id)):
                self.remove_edge(node_id, vert_out)
            for vert_in in list(self.all_in_edges_of_node(node_id)):
                self.remove_edge(vert_in, node_id)
            self._nodes.pop(node_id)
            self._edgeIn.pop(node_id)
            self._edgeOut.pop(node_id)
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self._nodes and node_id2 in self._nodes and self._edgeOut.get(node_id1).get(node_id2):
            self._edgeOut.get(node_id1).pop(node_id2)
            self._edgeIn.get(node_id2).pop(node_id1)
            self._edge_size = self._edge_size - 1
            self._mc = self._mc + 1
            return True
        return False

    def get_edge_out(self) -> dict:
        return self._edgeOut

    def get_edge_in(self) -> dict:
        return self._edgeIn
