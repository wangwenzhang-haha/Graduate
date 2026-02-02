"""PyG graph builder implementation.

PyG 图构建实现。
"""

from __future__ import annotations

from typing import Dict

import torch
from torch_geometric.data import HeteroData

from .base import build_edge_index, edge_schema


def build_graph_pyg(
    reviews: list[dict],
    metadata: dict[str, dict],
    entity_maps: dict[str, dict[str, int]],
    use_brand: bool = True,
    use_category: bool = True,
    add_node_ids: bool = True,
) -> HeteroData:
    """Build a PyG heterograph from reviews and metadata.

    使用评论与元数据构建 PyG 异构图。
    """
    data = HeteroData()

    # Register node counts from entity maps. / 根据实体映射注册节点数量。
    data["user"].num_nodes = len(entity_maps.get("user", {}))
    data["item"].num_nodes = len(entity_maps.get("item", {}))

    if use_brand:
        data["brand"].num_nodes = len(entity_maps.get("brand", {}))
    if use_category:
        data["category"].num_nodes = len(entity_maps.get("category", {}))

    # Optionally add node ID features. / 可选添加节点 ID 特征。
    if add_node_ids:
        data["user"].x = torch.arange(data["user"].num_nodes).unsqueeze(-1)
        data["item"].x = torch.arange(data["item"].num_nodes).unsqueeze(-1)
        if use_brand:
            data["brand"].x = torch.arange(data["brand"].num_nodes).unsqueeze(-1)
        if use_category:
            data["category"].x = torch.arange(data["category"].num_nodes).unsqueeze(-1)

    # Build edges following the shared schema. / 按统一结构构建边。
    for src_type, relation, dst_type in edge_schema:
        if relation == "produced_by" and not use_brand:
            continue
        if relation == "belongs_to" and not use_category:
            continue

        src_ids, dst_ids = build_edge_index(
            reviews=reviews,
            metadata=metadata,
            entity_maps=entity_maps,
            edge_type=(src_type, relation, dst_type),
        )
        edge_index = torch.tensor([src_ids, dst_ids], dtype=torch.long)
        data[(src_type, relation, dst_type)].edge_index = edge_index

    return data
