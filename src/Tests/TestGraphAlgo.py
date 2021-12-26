import copy
import unittest

import sys
import os

myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path

path = Path(myDir)
a = str(path.parent.absolute())

sys.path.append(a)
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from src.Tests.GraphCreator import GraphCreator


class MyTestCase(unittest.TestCase):
    def test_connected(self):
        g1 = GraphCreator(1, 0, 0)  # Graph without Edges without nodes have to be true
        graph1 = g1.create_graph()
        g_algo1 = GraphAlgo(graph1)
        self.assertEqual(True, g_algo1.connected())
        g1 = GraphCreator(1, 10, 0)  # Graph without Edges
        graph1 = g1.create_graph()
        g_algo1 = GraphAlgo(graph1)
        self.assertEqual(False, g_algo1.connected())
        g1 = GraphCreator(1, 5, 20)  # This graph is full connected graph have to be connected
        graph1 = g1.create_graph()
        g_algo1 = GraphAlgo(graph1)
        self.assertEqual(True, g_algo1.connected())  # This graph is full connected graph have to be connected
        g1 = GraphCreator(1, 10, 90)
        graph1 = g1.create_graph()
        g_algo1 = GraphAlgo(graph1)
        self.assertEqual(True, g_algo1.connected())
        g1 = GraphCreator(1, 100, 2000)
        graph1 = g1.create_graph()
        g_algo1 = GraphAlgo(graph1)
        self.assertEqual(True, g_algo1.connected())
        # g1 = GraphCreator(1, 1000, 20000)
        # graph1 = g1.create_graph()
        # g_algo1 = GraphAlgo(graph1)
        # self.assertEqual(True, g_algo1.connected())  # Big graphs
        # g1 = GraphCreator(1, 10000, 200000)
        # graph1 = g1.create_graph()
        # g_algo1 = GraphAlgo(graph1)
        # self.assertEqual(True, g_algo1.connected())  # Big graphs
        # g1 = GraphCreator(1, 100000, 2000000)
        # graph1 = g1.create_graph()
        # g_algo1 = GraphAlgo(graph1)
        # self.assertEqual(True, g_algo1.connected())
        # g1 = GraphCreator(1, 1000000, 20000000)  # Big graphs
        # graph1 = g1.create_graph()
        # g_algo1 = GraphAlgo(graph1)
        # self.assertEqual(True, g_algo1.connected())

    def test_shortest_path(self):
        g = DiGraph()
        graph_algo = GraphAlgo(g)
        graph_algo.load_from_json('../../data/A0.json')
        p, g = graph_algo.shortest_path(0, 5)
        self.assertEqual(g, [0, 1, 2, 3, 4, 5])

    def test_sub_graphs(self):
        g = DiGraph()
        graph_algo = GraphAlgo(g)
        graph_algo.load_from_json("../../data/subGraph.json")
        g.remove_edge(1, 0)
        dwg = graph_algo.build_graph_only_for_cities([2, 4, 6])
        self.assertEqual(dwg.v_size(), g.v_size() - 1)

    def test_all_center_jsons(self):

        graph_algo = GraphAlgo(DiGraph())
        graph_algo.load_from_json('../../data/A0.json')
        self.assertEqual((7, 6.806805834715163), graph_algo.centerPoint())
        graph_algo1 = GraphAlgo(DiGraph())
        graph_algo1.load_from_json('../../data/A1.json')
        self.assertEqual((8, 9.925289024973141), graph_algo1.centerPoint())
        graph_algo2 = GraphAlgo(DiGraph())
        graph_algo2.load_from_json('../../data/A2.json')
        self.assertEqual((0, 7.819910602212574), graph_algo2.centerPoint())
        graph_algo3 = GraphAlgo(DiGraph())
        graph_algo3.load_from_json('../../data/A3.json')
        self.assertEqual((2, 8.182236568942237), graph_algo3.centerPoint())
        graph_algo4 = GraphAlgo(DiGraph())
        graph_algo4.load_from_json('../../data/A4.json')
        self.assertEqual((6, 8.071366078651435), graph_algo4.centerPoint())
        graph_algo5 = GraphAlgo(DiGraph())
        graph_algo5.load_from_json('../../data/A5.json')
        self.assertEqual((40, 9.291743173960954), graph_algo5.centerPoint())


if __name__ == '__main__':
    unittest.main()
