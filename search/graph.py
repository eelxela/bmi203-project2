import networkx as nx
from collections import defaultdict
from typing import Union, Optional, List


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

    def _pick_shortest(self, path: List[list]) -> List[str]:
        """
        Flattens a list of lists into a list of strings that represents a shortest path.
        In the get_shortest_path fn we return a list of lists to allow for cycles such as (a-->b, a-->c, b-->d, c-->d)
        We will just flatten this list and select the first entry of each one so that we get a flat list of strings.

        Args:
            path (list of lists): List of lists, where each list has a node or multiple nodes.

        Returns:
            List of strings representing shortest path.
        """

        return [el[0] for el in path]

    def get_shortest_path(self, in_adj_map: dict, start: str, end: str) -> List[str]:
        """
        From a dictionary where the key: val pairs are nodes [key] and their parent nodes [vals], construct shortest path from start to end.

        Args:
            in_adj_map (dict): Dict of key: val pairs. Nodes are keys and parent nodes are values.
            start (str): Start node.
            end (str): End node.

        Returns:
            List of lists. The reason we return a list of lists is because we maintain cycles (ie if a-->b, a-->c, b-->d, c-->d).
            Then the return would be [[a], [b, c], [d]].
            We then can use _pick_shortest to just flatten the list and select one of the cycle nodes (b in the previous example), if they are present.
        """

        # initialize shortest path with the end node and the parent of end node
        shortest_path = [[end]] + [
            in_adj_map[end].copy()
        ]  # prevent from being popped out; since we are going to be popping elements out if we dont make a copy we'll be modifying our list values in place and weird things will happen

        if (
            start in in_adj_map[end]
        ):  # if its a path length of 1, then we just return start and the end node
            return [start] + shortest_path[0]

        """
        Neighbors will be initialized with the parent node of the end node as a list of length 1. We will use this list as a queue and pop off the last element, 
        continuing to add on the parents of the popped node, until we get to the start node.
        """
        neighbors = in_adj_map[
            end
        ].copy()  # needed so we don't modify the original list in in_adj_map

        while neighbors:
            node = neighbors.pop(-1)
            children = in_adj_map[node]  # get parent of node that was popped

            neighbors.extend(children)  # stick on the children to neighbors
            shortest_path.append(
                children
            )  # stick the children to the shortest path so far

            if start in children:
                break  # end

        return self._pick_shortest(
            reversed(shortest_path)
        )  # since we're going backwards through the list, we need to return it as a reversed list. see pick shortest for description of how we flatten this list of lists to a list of string

    def bfs(
        self,
        start: Union[int, str],
        end: Optional[Union[str, None]] = None,
    ):
        """
        Breadth-first search on networkx.DiGraph, from root node 'start'.
        If end is provided, then the search will end at node end and the return value will be a list of nodes corresponding to the shortest path.
        If not, the output will be the BFS traversal node order as a list of nodes.
        If start and end are provided, but start and end nodes are not connected, the output will be 'None'.

        A quick summary of the fn is that we are going to have a queue of nodes and a dictionary of node: node-neighbors pairs.
        We loop over the node: node-neighbors dict and for new/unseen nodes we add them to queue.
        Then for the nodes that entered queue, we make a new node: node-neighbors dict and we loop over that.
        We also record the parents of each node in a dictionary, so that if the user prompted we could backtrack that parent-node and get the shortest path.
        Eventually we will hit the end of the tree; and then we can return either the shortest path or the traversal.

        Args:
            start (str): Root node for the BFS.
            end (str, optional): Defaults to None. The end node for the BFS.

        Raises:
            ValueError: If the start node isn't a node in the graph.
            TypeError: If one of input arguments is wrong type (str for start, str/None for end)

        Returns:
            A list of nodes from start to end if start is provided and end are provided, and are connected.
            None if a start and end node are provided, but start and end are unconnected nodes.
            A traversal list of nodes if start is provided but not end.
        """

        if isinstance(start, (int, str)) is False:
            raise TypeError('Argument "start" must be a string or int.')

        if not (end is None or isinstance(end, (int, str))):
            raise TypeError('Argument "end" must be a string or "None".')

        if start not in self.nodes:
            raise ValueError(
                f"Provided node name: {start} not a valid node in the graph found at {self.filename}"
            )
        if (end is not None) and (end not in self.nodes):
            raise ValueError(
                f"Provided node name: {end} not a valid node in the graph found at {self.filename}"
            )

        if (end is not None) and (start == end):
            return [start]

        # initialize seen
        seen = [start]

        parents = defaultdict(
            list
        )  # keep defaultdict of lists for the parents of the nodes, so that we can backtrack and find shortest path if desired

        neighbors = {
            start: []
        }  # keep dict of neighbors to traverse as a queue; not sure if this is best way compared to just popping elements off list
        # my understanding from google'ing around is that this is faster but less space efficient for Python
        # key: val will be keys as nodes and vals as list of nodes neighbors of key [initialized with first order neighbors of start]

        for neighbor in sorted(
            self.graph.neighbors(start)
        ):  # populate neighobrs dict with the first order neighbors of start node
            neighbors[start].append(neighbor)
            parents[neighbor].append(start)

        finished = False

        while not finished:  # main loop
            queue = (
                []
            )  # so we can keep track of nodes that we need to explore from next depth level in tree
            for top_node in neighbors.keys():
                for top_node_neighbor in neighbors[top_node]:
                    # for the neighbors of top_node, we will add them to queue if we havent explored them yet
                    if (top_node_neighbor not in seen) and (
                        top_node_neighbor not in queue
                    ):
                        # print(top_node_neighbor)
                        queue.append(top_node_neighbor)

            queue.sort()
            seen.extend(queue)  # add new nodes to seen

            neighbors = (
                {}
            )  # new neighbors dict, we will populate this with the items in queue
            # will be key: val where key is nodes and val is neighbors as a list
            for node in queue:
                node_neighbors = sorted(self.graph.neighbors(node))
                neighbors[node] = node_neighbors
                for (
                    child_node
                ) in (
                    node_neighbors
                ):  # avoid symmetric links ; ie a cites b and b cites a
                    if (child_node in seen) or (node in parents[child_node]):
                        continue

                    parents[child_node].append(node)

            if (
                len(neighbors) == 0
            ):  # if we reach the end, given by no neighbors found, stop search
                break

            if (end is not None) and (end in seen):  # if we found end, also stop
                finished = True

        self.parents = parents  # store the parents, just for convenience

        # implement desired logic for the different types of returns
        if end is None:
            return seen
        elif (end is not None) and (finished is True):
            return self.get_shortest_path(parents, start, end)
        else:
            return None
