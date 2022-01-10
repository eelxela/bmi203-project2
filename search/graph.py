import networkx as nx
from collections import defaultdict


class Graph:
    """
    Class to contain a graph and your bfs function
    """

    def __init__(self, filename: str):
        """
        Initialization of graph object which serves as a container for
        methods to load data and

        """
        self.filename = filename
        self.graph = nx.read_adjlist(filename, create_using=nx.DiGraph, delimiter=";")
        self.nodes = self.graph.nodes

    def bfs(self, start: str, end: str = None):
        """
        SOLUTION: write a method that performs a breadth first traversal and pathfinding on graph G

        * If there's no end node, just return a list with the order of traversal
        * If there is an end node and a path exists, return a list of the shortest path
        * If there is an end node and a path does not exist, return None

        """

        if start not in self.nodes:
            raise ValueError(
                f"Provided node name: {start} not a valid node in the graph found at {self.filename}"
            )
        if (end is not None) and (end not in self.nodes):
            raise ValueError(
                f"Provided node name: {end} not a valid node in the graph found at {self.filename}"
            )

        depth = 1
        seen = {start: 0}

        parent_dict = defaultdict(list)
        finished = False
        neighbors = sorted(self.graph.neighbors(start))

        while finished is False:
            queue = set()
            for neighbor in neighbors:
                if neighbor not in seen.keys():
                    queue.add(neighbor)

            if end is not None and end in queue:
                break

            queue = sorted(queue)

            seen.update({node: depth for node in queue})

            neighbors = []

            for node in sorted(queue):
                # print(node, node in self.nodes)
                neighbors.extend(self.graph.neighbors(node))

            neighbors.sort()

            if len(neighbors) == 0:
                break  # end of graph traversal

            depth += 1

        return seen


import networkx as nx
from typing import Union


class Graph:
    """
    Class to contain a graph and your bfs function
    """

    def __init__(self, filename: str):
        """
        Initialization of graph object which serves as a container for
        methods to load data and

        """
        self.filename = filename
        self.graph = nx.read_adjlist(filename, create_using=nx.DiGraph, delimiter=";")
        self.nodes = self.graph.nodes

    def bfs(self, start: str, end: str = None):
        """
        SOLUTION: write a method that performs a breadth first traversal and pathfinding on graph G

        * If there's no end node, just return a list with the order of traversal
        * If there is an end node and a path exists, return a list of the shortest path
        * If there is an end node and a path does not exist, return None

        """

        if start not in self.nodes:
            raise ValueError(
                f"Provided node name: {start} not a valid node in the graph found at {self.filename}"
            )
        if (end is not None) and (end not in self.nodes):
            raise ValueError(
                f"Provided node name: {end} not a valid node in the graph found at {self.filename}"
            )

        depth = 0
        seen = tuple(sorted(self.neighbors(start)))
        finished = False

        for neighbor in neighbors:
            if neighbor not in seen:
                seen.append(neighbor)

            depth += 1

        return
