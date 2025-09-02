# Minimal FVS-FPT: An FPT Approach to the Feedback Vertex Set Problem

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package provides a Python implementation of a fixed-parameter tractable (FPT) algorithm for the **Feedback Vertex Set (FVS)** problem. The FVS problem is a classic challenge in graph theory that involves finding the smallest set of vertices to remove from a graph to make it acyclic (i.e., to eliminate all cycles).

This implementation is based on an iterative compression technique, which is a powerful method for designing FPT algorithms.

## Overview

The Feedback Vertex Set problem is NP-hard. However, by using a fixed-parameter tractable approach, we can solve the problem efficiently when the size of the desired feedback vertex set, `k`, is small. This package provides the necessary tools to compute the minimal FVS for a given graph.

The core of the algorithm relies on two key components:
1.  **FVS Compression**: A routine that, given an FVS of size `k+1`, attempts to find a smaller one of size `k`.
2.  **Disjoint FVS Solver**: A subroutine used by the compression step to find an FVS that is disjoint from a known FVS.

## Features

-   An iterative FPT algorithm for the Minimum Feedback Vertex Set problem.
-   A clear implementation of the FVS compression and disjoint FVS subproblems.
-   Built on top of the popular `networkx` library for easy graph manipulation.
-   Helper functions for generating test graphs with known FVS properties.

## Installation

You can install the package directly from PyPI:

```bash
pip install minimal_fvs_fpt
```

Ensure you have Python 3.11 or newer.

## How to Use

Here is a simple example of how to use the `MinimalFVSProblem` solver to find the minimum feedback vertex set of a graph.

```python
import networkx as nx
from minimal_fvs_fpt import MinimalFVSProblem

# 1. Create a graph with a few cycles.
# This graph is two triangles joined at vertex 3.
G = nx.Graph()
G.add_edges_from([
    (1, 2), (2, 3), (3, 1),  # First triangle
    (3, 4), (4, 5), (5, 3)   # Second triangle
])

# The minimal FVS for this graph is the single vertex {3}.

# 2. Create a solver instance with the graph.
problem = MinimalFVSProblem(G)

# 3. Solve the problem.
problem.solve()

# 4. Print the results.
print(f"The graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
print(f"The minimal Feedback Vertex Set is: {problem.X}")

# 5. Verify the solution.
# Removing the FVS should result in an acyclic graph (a forest).
remaining_nodes = [n for n in G.nodes() if n not in problem.X]
subgraph = G.subgraph(remaining_nodes)
is_forest = nx.is_forest(subgraph)

print(f"Is the remaining graph a forest? {is_forest}")

# Expected Output:
# The graph has 5 nodes and 6 edges.
# The minimal Feedback Vertex Set is: [3]
# Is the remaining graph a forest? True
```

## Algorithms and Components

-   `MinimalFVSProblem`: The main class that implements the iterative FPT algorithm.
-   `FVSCompressionProblem`: Solves the compression step of the FVS problem.
-   `DisjointFVSProblem`: Solves the problem of finding an FVS that is disjoint from a FVS `W`.

## Running Tests

To run the test suite for this package, navigate to the root directory and use the `unittest` discovery tool:

```bash
python -m unittest discover
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you find a bug or have a suggestion for improvement, please open an issue on the [GitHub Issues](https://github.com/vladimirminaev/Minimal-FVS-FPT/issues) page.

## References

The FPT algorithm implemented in this package is based on the iterative compression technique described by the following authors:

* Jianer Chen
* Fedor V. Fomin
* Yang Liu
* Songjian Lu
* Yngve Villanger
* **Paper:** ["Improved algorithms for feedback vertex set problems". In: Journal of
Computer and System Sciences](https://www.sciencedirect.com/science/article/pii/S0022000008000500)
