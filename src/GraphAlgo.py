from typing import List
import json
from src import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from NodeData import NodeData
from queue import PriorityQueue


def dfs(g: DiGraph, starting_node: NodeData):
    st = [starting_node]
    while len(st) > 0:
        curr_node = st.pop()
        curr_node.set_tag(1)
        for neigh in g.all_out_edges_of_node(curr_node.get_key()):
            neigh_node = g.get_node(neigh)
            if neigh_node.get_tag() == 0:
                st.append(neigh_node)


def check_graph_connectivity(g: DiGraph) -> bool:
    for node_data in g.get_all_v():
        curr = g.get_node(node_data)
        if curr.get_tag() == 0:
            return False
    return True


def graph_transposer(g: DiGraph) -> DiGraph:
    graph_trans = DiGraph()
    for node_id in g.get_all_v():
        graph_trans.add_node(node_id)
        for edge_id in g.all_out_edges_of_node(node_id):
            e = g.get_edge(node_id, edge_id)
            graph_trans.add_node(edge_id)
            graph_trans.add_edge(e.get_dest(), e.get_src(), e.get_weight())

    return graph_trans


def dijkstra(g: DiGraph, start, end=None):
    p = {}
    q = PriorityQueue()
    node = g.get_node(start)
    node.set_weight(0)
    q.put((node.get_weight(), node.get_key()))
    while not q.empty():
        curr_node = q.get()
        curr_key = curr_node[1]
        for neigh in g.all_out_edges_of_node(curr_key):
            e = g.get_edge(curr_key, neigh)
            if g.get_node(e.get_dest()).get_tag() == 0:
                neigh_node = g.get_node(neigh)
                weight = g.get_node(curr_key).get_weight() + e.get_weight()
                if weight < neigh_node.get_weight():
                    neigh_node.set_weight(weight)
                    p[neigh_node] = curr_key
                    q.put((neigh_node.get_weight(), neigh_node.get_key()))
            g.get_node(curr_key).set_tag(1)


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: DiGraph = None):
        if graph is not None:
            self._g = graph
        else:
            self._g = DiGraph()
        self._parent = {}

    def connected(self) -> bool:
        if self._g.get_all_v() is not None:
            starting_node = next(iter(self._g.get_all_v()))
            node = self._g.get_node(starting_node)
            g_trans = graph_transposer(self._g)
            for i in range(2):
                if i == 0:
                    dfs(self._g, node)
                    b = check_graph_connectivity(self._g)
                    if not b:
                        return False
                if i == 1:
                    dfs(g_trans, node)
                    b = check_graph_connectivity(g_trans)
                    if not b:
                        return False
        return True

    def get_graph(self) -> GraphInterface:
        return self._g

    def centerPoint(self) -> (int, float):
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'r+') as f:
                json_graph = json.load(f)
                for value in json_graph['Nodes']:
                    if len(value) > 1:
                        pos_str = str(value['pos'])
                        pos_arr = pos_str.split(',')
                        self._g.add_node(value['id'], (pos_arr[0], pos_arr[1], pos_arr[2]))
                    else:
                        self._g.add_node(value['id'])
                for edge in json_graph['Edges']:
                    self._g.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))
            return True
        except IOError as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        json_graph = {'Edges': [], 'Nodes': []}
        for node_data in self._g.get_all_v():
            node = self._g.get_node(node_data)
            if node.get_pos() is None:
                node_dict = {'id': node.get_key()}
                json_graph['Nodes'].append(node_dict)
            else:
                pos = str(node.get_pos()[0]) + ',' + str(node.get_pos()[1]) + ',' + str(node.get_pos()[2])
                node_dict = {'id': node.get_key(), 'pos': pos}
                json_graph['Nodes'].append(node_dict)

        for node in self._g.get_all_v():
            for edge in self._g.all_out_edges_of_node(node):
                e = self._g.get_edge(node, edge)
                edge_dict = {'src': e.get_src(), 'w': e.get_weight(), 'dest': e.get_dest()}
                json_graph['Edges'].append(edge_dict)

        graph = json.dumps(json_graph, indent=2)
        print(graph)
        try:
            with open(file_name, 'w') as f:
                f.write(graph)
                return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def plot_graph(self) -> None:
        pass
