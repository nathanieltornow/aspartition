# Graph Partitioning with Answer Set Programming

A Python package that provides a way to find an optimal graph partition into *n* subgraphs using the [**clingo**](https://potassco.org/clingo/) answer set programming solver.
This partitioning works for unidirected graphs with weighted nodes and weighted edges. The partitioning is done so that the weight-distribution of nodes is optimal and the total weights of edges between partitions is minimal.

## Installation

- Install clingo via [https://github.com/potassco/clingo/releases/](https://github.com/potassco/clingo/releases/).

- Install this package
  ```shell
  git clone https://github.com/nathanieltornow/aspartition.git
  cd aspartition
  pip install .
  ```

## Example

```python
import networkx as nx
from aspartition import partition_graph

# create com graph (with weights and nodes being integers!)
G = nx.Graph()
G.add_edge(1, 2, weight=6)
G.add_edge(1, 3, weight=2)
G.add_edge(3, 4, weight=1)
G.add_edge(3, 5, weight=7)
G.add_edge(3, 6, weight=9)
G.add_edge(1, 4, weight=3)

print(partition_graph(graph=G, num_partitions=3))
```