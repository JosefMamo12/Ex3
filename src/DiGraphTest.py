import unittest

from GraphCreator import GraphCreator
from NodeData import NodeData


class MyTestCase(unittest.TestCase):
    def test_add_get_node(self):
        num_of_nodes = 1000
        num_of_edges = 200000
        graph = GraphCreator(0, num_of_nodes, num_of_edges)
        g = graph.create_graph()
        self.assertEqual(g.v_size(), num_of_nodes)  #
        pos = g.get_node(num_of_nodes - 1).get_pos()
        node = NodeData(num_of_nodes - 1)
        node.set_pos(pos[0], pos[1], pos[2])
        self.assertEqual(g.get_node(num_of_nodes - 1), node)
        self.assertEqual(None, g.get_node(num_of_nodes))
        g.add_node(num_of_nodes, (35.013013232, 32.13232323, 0))
        self.assertEqual(num_of_nodes + 1, g.v_size())

    def test_add_edge(self):
        num_of_nodes = 100
        num_of_edges = 2000
        graph = GraphCreator(0, num_of_nodes, num_of_edges)
        g = graph.create_graph()
        self.assertEqual(num_of_edges, g.e_size())


    def test_remove_edge(self):
        num_of_nodes = 5
        num_of_edges = 20
        graph = GraphCreator(0, num_of_nodes, num_of_edges)  # Means that the specific graph is Complete Graph
        g = graph.create_graph()
        self.assertEqual(True, g.remove_edge(0, 1))
        self.assertEqual(num_of_edges - 1, g.e_size())
        for key in g.get_all_v():
            for value in list(g.all_out_edges_of_node(key)):
                g.remove_edge(key, value)
        print(g.get_edge_out())
        self.assertEqual(0, g.e_size())

    def test_remove_node(self):
        num_of_nodes = 3
        num_of_edges = 6
        graph = GraphCreator(0, num_of_nodes, num_of_edges)  # Means that the specific graph is Complete Graph
        g = graph.create_graph()
        self.assertEqual(g.v_size(), 3)
        self.assertEqual(False, g.remove_node(5))
        for node_id in list(g.get_all_v()):
            g.remove_node(node_id)
        self.assertEqual(g.v_size(), 0)
        self.assertEqual(g.e_size(), 0)
        self.assertEqual(False, g.remove_node(32))


if __name__ == '__main__':
    unittest.main()
