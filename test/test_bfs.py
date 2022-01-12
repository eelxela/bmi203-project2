# write tests for bfs
import pathlib
import pytest
from search import graph


TRAVERSAL_ORDER = [
    "Martin Kampmann",
    "31540829",
    "31626775",
    "31806696",
    "32790644",
    "33483487",
    "Lani Wu",
    "Luke Gilbert",
    "Neil Risch",
    "Nevan Krogan",
    "Steven Altschuler",
    "29700475",
    "30727954",
    "30944313",
    "32036252",
    "32042149",
    "32353859",
    "34272374",
    "Atul Butte",
    "Hani Goodarzi",
    "Marina Sirota",
    "Michael Keiser",
    "Michael McManus",
    "31395880",
    "31486345",
    "32025019",
    "33232663",
    "33242416",
    "33765435",
    "Charles Chiu",
]

# copy pasted from inspecting my output and nx.bfs traversal fn and finding unconnected nodes
UNCONNECTED_NODES = {
    "34916529": ["34858697", "34816322", "34803213", "34754064", "34675264"],
    "34855188": ["34946917", "34946911", "34946904", "34946875", "34946870"],
}

# copy pasted from inspecting my output and nx.bfs traversal fn
CONNECTED_NODES = {
    "Martin Kampmann": ["34888545", "34912531", "34919578", "34945766", "34957251"],
    "Charles Chiu": ["34883951", "34912531", "34919578", "34945766", "34957251"],
}

ER_CONNECTS = (("0", "7", 4), ("1", "5", 3), ("4", "5", 3))
ER_UNCONNECT = (("6", "0"), ("3", "5"))


@pytest.fixture
def er_graph():
    fname = (
        pathlib.Path(__file__).resolve().parent.parent / "test" / "erdosrenyi.adjlist"
    )
    return graph.Graph(fname)


@pytest.fixture
def tiny_graph():
    # returns a graph.Graph object from tiny_network.adjlist
    fname = (
        pathlib.Path(__file__).resolve().parent.parent / "data" / "tiny_network.adjlist"
    )
    return graph.Graph(fname)


@pytest.fixture
def big_graph():
    # returna a graph.Graph object from citation_network.adjlist
    fname = (
        pathlib.Path(__file__).resolve().parent.parent
        / "data"
        / "citation_network.adjlist"
    )
    return graph.Graph(fname)


def test_bfs_traversal(tiny_graph):
    """
    TODO: Write your unit test for a breadth-first
    traversal here. Create an instance of your Graph class
    using the 'tiny_network.adjlist' file and assert
    that all nodes are being traversed (ie. returns
    the right number of nodes, in the right order, etc.)
    """

    traversal = tiny_graph.bfs(start="Martin Kampmann")
    assert traversal == TRAVERSAL_ORDER  # same order
    assert len(traversal) == len(TRAVERSAL_ORDER)  # same number
    assert len(traversal) == len(tiny_graph.nodes)  # all nodes included


def test_bfs(big_graph, er_graph):
    """
    TODO: Write your unit test for your breadth-first
    search here. You should generate an instance of a Graph
    class using the 'citation_network.adjlist' file
    and assert that nodes that are connected return
    a (shortest) path between them.

    Include an additional test for nodes that are not connected
    which should return None.
    """

    # for any of first five nodes, check that the neighbors have a path
    for node in list(big_graph.nodes)[:5]:
        neighbors = big_graph.graph.neighbors(node)
        for neighbor in neighbors:
            bfs = big_graph.bfs(start=node, end=neighbor)
            assert bfs is not None
            assert len(bfs) == 2

    # all of connectected nodes shouhld have a path
    for node, connected_nodes in CONNECTED_NODES.items():
        for connected_node in connected_nodes:
            bfs = big_graph.bfs(start=node, end=connected_node)
            # fmt: off
            check = ((bfs is not None) and len(bfs) > 1) # black formatter wants to elide this into one check
            assert check
            # fmt: on

    # all of unconnected nodes should not have a path
    for node, unconnected_nodes in UNCONNECTED_NODES.items():
        for unconnected_node in unconnected_nodes:
            bfs = big_graph.bfs(start=node, end=unconnected_node)
            assert bfs is None

    assert big_graph.bfs("Martin Kampmann", "Martin Kampmann") == ["Martin Kampmann"]

    with pytest.raises(ValueError, match=r"not a valid node in the graph"):
        big_graph.bfs("Somebody")
        big_graph.bfs("Martin Kampmann", "Nobody")

    with pytest.raises(TypeError, match=r'Argument "end" must be a string or "None"'):
        big_graph.bfs("Martin Kampmann", [])

    with pytest.raises(TypeError, match=r'Argument "start" must be a string or int.'):
        big_graph.bfs(3.2)
        
    # test mini erdos-renyi graph, see erdosrenyi.png for image
    # path lengths found by inspection
    for (start, end, length) in ER_CONNECTS:
        path = er_graph.bfs(start=start, end=end)
        assert length == len(path)

    for (start, end) in ER_UNCONNECT:  # these nodes unconnected in ergraph.png
        path = er_graph.bfs(start=start, end=end)
        assert path is None
