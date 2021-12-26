import copy

from typing import List
import json

from src import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from NodeData import NodeData
from queue import PriorityQueue
import sys


def clean(g: DiGraph) -> None:
    if g is not None:
        for key in g.get_all_v():
            g.get_node(key).set_tag(0)
            g.get_node(key).set_weight(sys.float_info.max)
            g.get_node(key).set_info('')


def dfs(g: DiGraph, starting_node: NodeData):
    clean(g)
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


class GraphAlgo(GraphAlgoInterface):

    def reset(self):
        if self._g.get_all_v():
            self._g.get_all_v().clear()
            self._g.get_edge_out().clear()
            self._g.get_edge_in().clear()

    def graph_transposer(self) -> DiGraph:
        graph_trans = DiGraph()
        for node_id in self._g.get_all_v():
            graph_trans.add_node(node_id)
            for edge_id in self._g.all_out_edges_of_node(node_id):
                graph_trans.add_node(edge_id)
                graph_trans.add_edge(edge_id, node_id, self._g.all_out_edges_of_node(node_id).get(edge_id))
        return graph_trans

    def dijkstra(self, start, end=None):
        clean(self._g)
        p = {}
        q = PriorityQueue()
        node = self._g.get_node(start)
        node.set_weight(0)
        q.put((node.get_weight(), node.get_key()))
        while not q.empty():
            curr_node = q.get()
            curr_key = curr_node[1]
            if end is not None and curr_key == end:
                break
            for neigh in self._g.all_out_edges_of_node(curr_key):
                if self._g.get_node(neigh).get_tag() == 0:
                    neigh_node = self._g.get_node(neigh)
                    weight = self._g.get_node(curr_key).get_weight() + self._g.all_out_edges_of_node(curr_key).get(
                        neigh)
                    if weight < neigh_node.get_weight():
                        neigh_node.set_weight(weight)
                        p[neigh] = curr_key
                        q.put((neigh_node.get_weight(), neigh_node.get_key()))
                self._g.get_node(curr_key).set_tag(1)
        if end is not None:
            return p, self._g.get_node(end).get_weight()

    def __init__(self, graph: DiGraph = None):
        if graph is not None:
            self._g = graph
        else:
            self._g = DiGraph()
        self._parent = {}

    def connected(self) -> bool:
        if self._g.get_all_v() is not None:
            g_trans = self.graph_transposer()
            for i in range(2):
                if i == 0:
                    starting_node = next(iter(self._g.get_all_v()))
                    node = self._g.get_node(starting_node)
                    dfs(self._g, node)
                    b = check_graph_connectivity(self._g)
                    if not b:
                        return False
                if i == 1:
                    starting_node = next(iter(g_trans.get_all_v()))
                    node = g_trans.get_node(starting_node)
                    dfs(g_trans, node)
                    b = check_graph_connectivity(g_trans)
                    if not b:
                        return False
        return True

    def get_graph(self) -> GraphInterface:
        return self._g

    def centerPoint(self) -> (int, float):
        clean(self._g)
        if self.connected():
            center = None
            highest_dist = sys.float_info.max
            for curr in self._g.get_all_v():
                dist = sys.float_info.min
                self.dijkstra(curr)
                for dist_curr in self._g.get_all_v():
                    temp_dist = self._g.get_node(dist_curr).get_weight()
                    if temp_dist > dist:
                        dist = temp_dist
                if dist < highest_dist:
                    highest_dist = dist
                    center = curr
            self._g.get_node(center).set_info('Paint')
            return center, highest_dist
        return -1, float('inf')

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        clean(self._g)
        if node_lst is None or len(node_lst) == 1:
            return [], -1
        if len(node_lst) == 2:
            if self.shortest_path(node_lst[0], node_lst[1])[0] > self.shortest_path(node_lst[1], node_lst[0])[0]:
                return self.shortest_path(node_lst[1], node_lst[0])
            else:
                return self.shortest_path(node_lst[0], node_lst[1])
        for node in node_lst:
            if node not in self._g.get_all_v():
                return [], -1
        graph_for_tsp = self.build_graph_only_for_cities(node_lst)
        graph_algo = GraphAlgo(graph_for_tsp)
        if graph_algo.connected():

            ans1 = list()
            ans2 = list()

            shortest_path_dist_1 = 0
            shortest_path_dist_2 = 0

            right = self.find_the_rightest_node(node_lst)
            left = self.find_the_leftest_node(node_lst)

            for i in range(2):
                if i == 0:
                    n = right
                else:
                    n = left
                temp_list = copy.deepcopy(node_lst)
                while len(temp_list) > 1:
                    temp_list.remove(n)
                    next_elem = self.search_for_closest_node(n, temp_list)
                    if next_elem is not None:
                        if i == 0:
                            shortest_path_dist_1 += self.shortest_path(n, next_elem[0])[0]
                        else:
                            shortest_path_dist_2 += self.shortest_path(n, next_elem[0])[0]
                    temp_ans1 = self.shortest_path(n, next_elem[0])[1]
                    for elem in temp_ans1:
                        if i == 0:
                            ans1.append(elem)
                        else:
                            ans2.append(elem)
                    if len(temp_list) > 1:
                        if i == 0:
                            ans1.pop()
                        else:
                            ans2.pop()
                    n = next_elem[0]
                temp_list.clear()

            if shortest_path_dist_1 < shortest_path_dist_2:
                for node in ans1:
                    self._g.get_node(node).set_info('Paint')
                return ans1, shortest_path_dist_1
            for node in ans2:
                self._g.get_node(node).set_info('Paint')
            return ans2, shortest_path_dist_2
        else:
            temp_ans = list()
            ans = list()
            max_dist = sys.maxsize
            for node in node_lst:
                temp_ans.clear()
                dist = 0
                temp_lst = copy.deepcopy(node_lst)
                curr = node
                while len(temp_lst) > 1:
                    temp_lst.remove(curr)
                    next_node, next_dist = self.search_for_closest_node(curr, temp_lst)
                    if next_node == -1:
                        dist = sys.maxsize
                        break
                    dist += next_dist
                    temp_ans1 = self.shortest_path(curr, next_node)[1]
                    for elem in temp_ans1:
                        temp_ans.append(elem)
                    if len(temp_lst) > 1:
                        temp_ans.pop()
                    curr = next_node
                if dist < max_dist:
                    max_dist = dist
                    ans = copy.deepcopy(temp_ans)
            for node in ans:
                self._g.get_node(node).set_info('Paint')
            return max_dist, ans

    def build_graph_only_for_cities(self, node_lst: List[int]) -> DiGraph:
        dwg = DiGraph()
        temp_cities = copy.deepcopy(node_lst)
        for city in temp_cities:
            if not dwg.get_all_v() or city not in dwg.get_all_v():
                dwg.add_node(city)
            for neigh in self._g.all_out_edges_of_node(city):
                e_weight = self._g.all_out_edges_of_node(city).get(neigh)
                if neigh not in dwg.get_all_v():
                    dwg.add_node(neigh)
                    if neigh not in temp_cities:
                        temp_cities.append(neigh)
                dwg.add_edge(city, neigh, e_weight)
        return dwg

    def load_from_json(self, file_name: str) -> bool:
        self.reset()
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
                edge_dict = {'src': node, 'w': self._g.all_out_edges_of_node(node).get(edge), 'dest': edge}
                json_graph['Edges'].append(edge_dict)

        graph = json.dumps(json_graph, indent=2)
        try:
            with open(file_name, 'w') as f:
                f.write(graph)
                return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if not id1 in self._g.get_all_v() or id2 not in self._g.get_all_v():
            return float('inf'), []
        p, d = self.dijkstra(id1, id2)
        path = []
        if d != sys.float_info.max:
            while True:
                path.append(id2)
                if id1 == id2:
                    break
                id2 = p[id2]
            path.reverse()
            for node in path:
                self._g.get_node(node).set_info('Paint')
            return d, path
        return float('inf'), path

    def plot_graph(self) -> None:
        from src.Gui.DrawGraph import GraphDraw
        gd = GraphDraw(self)
        gd.run_gui()

    def find_the_rightest_node(self, node_lst):
        rightest_index = 0
        rightest_value = 0
        for city in node_lst:
            x = self._g.get_node(city).get_pos()[0]
            if x > rightest_value:
                rightest_value = x
                rightest_index = city
        return rightest_index

    def find_the_leftest_node(self, node_lst):
        leftest_index = 0
        leftest_value = sys.float_info.max
        for city in node_lst:
            x = self._g.get_node(city).get_pos()[0]
            if x < leftest_value:
                leftest_value = x
                leftest_index = city
        return leftest_index

    def search_for_closest_node(self, n, temp_list):
        min_dist = sys.float_info.max
        closest_node = -1
        for curr in temp_list:
            temp_dist = self.shortest_path(n, curr)[0]
            if min_dist > temp_dist:
                min_dist = temp_dist
                closest_node = curr
        return closest_node, min_dist
