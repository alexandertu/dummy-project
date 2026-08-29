"""networkx: graph construction and traversal algorithms."""

import networkx as nx
import pytest

pytestmark = pytest.mark.heavy


@pytest.fixture
def graph() -> nx.Graph:
    g = nx.Graph()
    g.add_edges_from([("a", "b"), ("b", "c"), ("c", "d"), ("a", "d"), ("d", "e")])
    return g


def test_order_and_size(graph: nx.Graph) -> None:
    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 5


def test_shortest_path(graph: nx.Graph) -> None:
    assert nx.shortest_path(graph, "a", "e") == ["a", "d", "e"]
    assert nx.shortest_path_length(graph, "a", "c") == 2


def test_degree(graph: nx.Graph) -> None:
    assert graph.degree["d"] == 3
    assert graph.degree["e"] == 1


def test_connected_components(graph: nx.Graph) -> None:
    graph.add_edge("x", "y")  # a second, disjoint component
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    assert len(components) == 2
    assert len(components[0]) == 5
    assert components[1] == {"x", "y"}


def test_pagerank_sums_to_one(graph: nx.Graph) -> None:
    ranks = nx.pagerank(graph)
    assert sum(ranks.values()) == pytest.approx(1.0)
    # 'd' has the highest degree, so it should rank highest.
    assert max(ranks, key=ranks.get) == "d"
