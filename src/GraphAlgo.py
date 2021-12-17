from typing import List

import json
import pandas as pd
from src import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph: DiGraph = None):
        self._g = DiGraph()
        if graph is not None:
            self._g = graph

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
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):

        pass

    def plot_graph(self) -> None:

        pass
