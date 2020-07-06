# 6.0002 Problem Set 5
# Graph optimization
# Name: Yaacoub Yaacoub
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge


#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# The graph's nodes represent every building at MIT (the source building)
# The nodes represent the destination from the source, and it also includes the distance outdoor and the total distance.
# the distances are represented in the edge string: - the first item in the bracket is the total distance,
#                                                   - the second item is the total outdoor distance.


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    print("Loading map from file...")
    map_file = open(map_filename, "r")
    map_entries = []
    for entry in map_file.readlines():
        map_entries.append(entry[:-1].split(" "))
    map_entries.sort()
    graph = Digraph()
    for entry in map_entries:
        try:
            graph.add_node(Node(entry[0]))
        except:
            pass
        try:
            graph.add_node(Node(entry[1]))
        except:
            pass
        try:
            graph.add_edge(WeightedEdge(Node(entry[0]), Node(entry[1]), int(entry[2]), int(entry[3])))
        except:
            pass
    map_file.close()
    return graph


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#
# g = load_map("test_load_map.txt")
# print(g)
# print()
# print("Nodes", g.get_nodes())
# print()
# for q in g.get_edges_for_node(Node('a')):
#     print(q)
#     b = q.get_destination()
#     print(b)
#     print(type(q))
#     print(type(b))
#     z1 = q.get_outdoor_distance()
#     print("Outdoor distance:", z1)
#     z2 = q.get_total_distance()
#     print("Total distance:", z2)
#     print()
#


# Problem 3: Finding the Shortest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective function of this problem is to minimize the to total distance traveled
# The constraint is the maximum distance spent outside should not exceed a given distance.


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    start = Node(start)
    end = Node(end)
    path = path + [start]
    # print("path", path)

    if start == end:
        # print("s=e")
        return path

    # nodes = digraph.get_edges_for_node(start)
    # print("nodes:", end=" ")
    # for n in nodes:
    #     print(n, end=", ")
    # print("done")

    for node in digraph.get_edges_for_node(start):
        # print("node:", node)
        if node.get_destination() not in path:
            # print(node.get_destination(), "is node not in path")
            newPath = get_best_path(digraph, node.get_destination(), end, path, max_dist_outdoors, best_dist, best_path)
            # print("new Path:", newPath)
            if newPath is not None:
                current_distance_outdoors = distance_outdoors(digraph, newPath)
                current_distance_total = current_distance(digraph, newPath)
                # print("current_distance_outdoors:", current_distance_outdoors)
                # print("current_distance:", current_distance_total)
                if (best_dist == 0) or ((current_distance_outdoors <= max_dist_outdoors) and (current_distance_total <=
                                                                                              best_dist)):
                    # print("IN")
                    best_dist = current_distance_total
                    best_path = newPath
                    # print("best_dist:", best_dist)
                    # print("best_path:", best_path)

    # print("best_distance:", best_dist)
    if len(best_path) == 0:
        return None
    else:
        return best_path


def distance_outdoors(digraph, path):
    outdoor_distance = 0
    for p in range(len(path) - 1):
        for edge in digraph.get_edges_for_node(path[p]):
            if edge.get_destination() == path[p + 1]:
                outdoor_distance = outdoor_distance + edge.get_outdoor_distance()
    return outdoor_distance


def current_distance(digraph, path):
    total_distance = 0
    for p in range(len(path) - 1):
        for edge in digraph.get_edges_for_node(path[p]):
            if edge.get_destination() == path[p + 1]:
                total_distance = total_distance + edge.get_total_distance()
    return total_distance


# print(get_best_path(load_map("mit_map.txt"), "2", "10", [], 10, 0, []))
# print(get_best_path(load_map("test_load_map.txt"), "a", "d", [], 5, 0, []))


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    path = get_best_path(digraph, start, end, [], max_dist_outdoors, max_total_dist, [])
    if path is None:
        raise ValueError("No path")
    else:
        path_toReturn = []
        for p in path:
            path_toReturn.append(str(p))
        return path_toReturn


# print(directed_dfs(load_map("mit_map.txt"), "32", "56", 200, 0))
# print(directed_dfs(load_map("test_load_map.txt"), "e", "b", 100, 30))

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
