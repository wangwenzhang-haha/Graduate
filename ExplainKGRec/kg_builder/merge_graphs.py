"""Merge subgraphs into a unified heterograph.

合并子图为统一的异构图。
"""

from __future__ import annotations

from typing import List

import dgl
from dgl import DGLHeteroGraph


def merge_graphs(
    base_graph: DGLHeteroGraph,
    external_graphs: List[DGLHeteroGraph],
    node_types: List[str],
    edge_types: List[str],
) -> DGLHeteroGraph:
    """Merge external graphs into the base heterograph.

    将外部图谱合并到基准异构图中。
    """
    # Collect all graphs to merge. / 收集待合并的图列表。
    graphs = [base_graph] + list(external_graphs)
    # Merge graphs using DGL batch/merge utility. / 使用 DGL 合并工具融合图结构。
    merged_graph = dgl.merge(graphs)

    # Ensure target node types exist. / 确保目标节点类型存在。
    for node_type in node_types:
        if node_type not in merged_graph.ntypes:
            raise ValueError(f"Missing node type after merge: {node_type}")

    # Ensure target edge types exist. / 确保目标边类型存在。
    for edge_type in edge_types:
        if edge_type not in {etype[1] for etype in merged_graph.canonical_etypes}:
            raise ValueError(f"Missing edge type after merge: {edge_type}")

    return merged_graph


def merge_node_features(
    base_graph: DGLHeteroGraph,
    external_graphs: List[DGLHeteroGraph],
    node_types: List[str],
) -> DGLHeteroGraph:
    """Merge node features from external graphs into the base graph.

    将外部图谱的节点特征合并到基准图中。
    """
    # Iterate through external graphs to merge features. / 遍历外部图以合并特征。
    for graph in external_graphs:
        for node_type in node_types:
            if node_type not in graph.ntypes:
                continue
            # Copy node features for each node type. / 复制每个节点类型的特征。
            for feature_name, feature_value in graph.nodes[node_type].data.items():
                base_graph.nodes[node_type].data[feature_name] = feature_value
    return base_graph
