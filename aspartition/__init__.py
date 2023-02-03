import networkx as nx
import posixpath
import subprocess
import os
import re


TMP_DIR = "./.tmp"
CLINGO_RULES_FILE = "graph_partition.lp"
CLINGO_INPUT_FILE = posixpath.join(TMP_DIR, "clingo_input.lp")
CLINGO_OUTPUT_FILE = posixpath.join(TMP_DIR, "clingo_output.txt")
PATTERN = re.compile(r"partition\(\s*(\d+)\s*,\s*(\d+)\s*\)", flags=re.ASCII)


def networkx_to_asp_str(graph: nx.Graph) -> str:
    """
    Converts a networkx graph with weighted vertices and weighted
    edges to a string in ASP format.
    """
    asp_str = ""
    for node, data in graph.nodes(data=True):
        if "weight" not in data:
            asp_str += f"vertex({node}, 1).\n"
        else:
            asp_str += f'vertex({node}, {data["weight"]}).\n'
    for u, v, data in graph.edges(data=True):
        if "weight" not in data:
            asp_str += f"edge({u}, {v}, 1).\n"
        else:
            asp_str += f'edge({u}, {v}, {data["weight"]}).\n'
    return asp_str


def parse_asp_result(asp_output: str, num_partitions: int) -> list[set[int]]:
    final_matches = []
    for line in asp_output.splitlines():
        matches = [(int(match[0]), int(match[1])) for match in PATTERN.findall(line)]
        if matches:
            final_matches = matches
    partitions = [set() for _ in range(num_partitions)]
    for node, partition in final_matches:
        partitions[partition - 1].add(node)
    return partitions


def partition_graph(graph: nx.Graph, num_partitions: int) -> list[set[int]]:
    asp_str = networkx_to_asp_str(graph)
    os.makedirs(TMP_DIR, exist_ok=True)

    with open(CLINGO_INPUT_FILE, "w") as f:
        print("Writing...")
        f.write(asp_str)
    clingo_command = f"clingo -c num_partitions={num_partitions} {CLINGO_RULES_FILE} {CLINGO_INPUT_FILE} --outf=1 > {CLINGO_OUTPUT_FILE}"
    subprocess.run(clingo_command, shell=True)
    with open(CLINGO_OUTPUT_FILE, "r") as f:
        asp_output = f.read()
        result = parse_asp_result(asp_output, num_partitions)
        return result
