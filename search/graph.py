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

    def _pick_shortest(self, path):
        """[summary]

        Args:
            path ([type]): [description]

        Returns:
            [type]: [description]
        """

        return [el[0] for el in path]

    def get_shortest_path(self, in_adj_map: dict, start: str, end: str):
        """[summary]

        Args:
            in_adj_map (dict): [description]
            start (str): [description]
            end (str): [description]

        Returns:
            [type]: [description]
        """

        shortest_path = [[end]] + [
            in_adj_map[end].copy()
        ]  # also prevent from being popped out

        if start in in_adj_map[end]:
            return [start] + shortest_path[0]

        neighbors = in_adj_map[
            end
        ].copy()  # needed so we don't modify the original list in in_adj_map

        while neighbors:
            node = neighbors.pop(-1)
            children = in_adj_map[node]

            neighbors.extend(children)
            shortest_path.append(children)

            if start in children:
                break

        return list(reversed(shortest_path))

    def bfs(self, start: str, end: str = None, return_reverse_adj: bool = False):
        """[summary]

        Args:
            start (str): [description]
            end (str, optional): [description]. Defaults to None.
            return_reverse_adj (bool, optional): [description]. Defaults to False.

        Raises:
            ValueError: [description]
            ValueError: [description]

        Returns:
            [type]: [description]
        """

        if isinstance(start, str) is False:
            raise TypeError('Argument "start" must be a string.')

        if not (end is None or isinstance(end, str)):
            raise TypeError('Argument "end" must be of a string or "None".')

        if start not in self.nodes:
            raise ValueError(
                f"Provided node name: {start} not a valid node in the graph found at {self.filename}"
            )
        if (end is not None) and (end not in self.nodes):
            raise ValueError(
                f"Provided node name: {end} not a valid node in the graph found at {self.filename}"
            )

        seen = [start]

        parents = defaultdict(list)

        neighbors = {start: []}
        for neighbor in sorted(self.graph.neighbors(start)):
            neighbors[start].append(neighbor)
            parents[neighbor].append(start)

        finished = False

        while not finished:
            queue = []
            for top_node in neighbors.keys():
                for top_node_neighbor in neighbors[top_node]:
                    if (top_node_neighbor not in seen) and (
                        top_node_neighbor not in queue
                    ):
                        # print(top_node_neighbor)
                        queue.append(top_node_neighbor)

            queue.sort()
            seen.extend(queue)

            neighbors = {}
            for node in queue:
                node_neighbors = sorted(self.graph.neighbors(node))
                neighbors[node] = node_neighbors
                for child_node in node_neighbors:
                    if (child_node in seen) or (node in parents[child_node]):
                        continue

                    parents[child_node].append(node)

            if len(neighbors) == 0:
                break

            if (end is not None) and (end in seen):
                finished = True

        self.parents = parents

        if end is None:
            return seen
        elif (end is not None) and (finished is True):
            return self._pick_shortest(self.get_shortest_path(parents, start, end))
        else:
            return None
