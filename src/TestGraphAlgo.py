import unittest

from GraphCreator import GraphCreator
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph


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
        graph_algo.load_from_json("../data/A0.json")
        print(graph_algo.connected())
        p, g = graph_algo.shortest_path(0, 5)
        print(p)
        print(g)


if __name__ == '__main__':
    unittest.main()
