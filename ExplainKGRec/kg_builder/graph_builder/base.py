"""Base interfaces for graph builders.

图构建器的基础接口。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Protocol, Sequence, Tuple

# Type aliases for node and edge identifiers. / 节点与边标识的类型别名。
NodeType = str
EdgeType = Tuple[NodeType, str, NodeType]

# Default edge schema for the KG builder. / 知识图谱的默认边类型结构。
edge_schema: List[EdgeType] = [
    ("user", "buys", "item"),
    ("item", "belongs_to", "category"),
    ("item", "produced_by", "brand"),
]


@dataclass(frozen=True)
class EdgeIndex:
    """Edge index representation for heterogeneous graphs.

    异构图的边索引表示。
    """

    src: Iterable[int]
    dst: Iterable[int]


@dataclass(frozen=True)
class GraphSchema:
    """Graph schema container describing node/edge types.

    描述节点/边类型的图结构容器。
    """

    node_types: Tuple[str, ...]
    edge_types: Tuple[str, ...]


GraphData = Dict[str, EdgeIndex]


def build_edge_index(
    reviews: Sequence[dict],
    metadata: Dict[str, dict],
    entity_maps: Dict[str, Dict[str, int]],
    edge_type: EdgeType,
) -> Tuple[List[int], List[int]]:
    """Build edge indices for a given edge type.

    为指定边类型构建边索引列表。
    """
    src_type, relation, dst_type = edge_type
    src_ids: List[int] = []
    dst_ids: List[int] = []

    if (src_type, relation, dst_type) == ("user", "buys", "item"):
        # Build user-item edges from reviews. / 从评论构建用户-物品边。
        user_map = entity_maps.get("user", {})
        item_map = entity_maps.get("item", {})
        for row in reviews:
            user = row.get("user")
            item = row.get("item")
            if user in user_map and item in item_map:
                src_ids.append(user_map[user])
                dst_ids.append(item_map[item])
        return src_ids, dst_ids

    if (src_type, relation, dst_type) == ("item", "belongs_to", "category"):
        # Build item-category edges from metadata. / 从元数据构建物品-类别边。
        item_map = entity_maps.get("item", {})
        category_map = entity_maps.get("category", {})
        for item_id, info in metadata.items():
            if not isinstance(info, dict):
                continue
            categories = info.get("categories", [])
            if item_id in item_map and isinstance(categories, list):
                for category in categories:
                    if category in category_map:
                        src_ids.append(item_map[item_id])
                        dst_ids.append(category_map[category])
        return src_ids, dst_ids

    if (src_type, relation, dst_type) == ("item", "produced_by", "brand"):
        # Build item-brand edges from metadata. / 从元数据构建物品-品牌边。
        item_map = entity_maps.get("item", {})
        brand_map = entity_maps.get("brand", {})
        for item_id, info in metadata.items():
            if not isinstance(info, dict):
                continue
            brand = info.get("brand")
            if item_id in item_map and brand in brand_map:
                src_ids.append(item_map[item_id])
                dst_ids.append(brand_map[brand])
        return src_ids, dst_ids

    # Unsupported edge types return empty edges. / 未支持的边类型返回空列表。
    return src_ids, dst_ids


class GraphBuilderBase(Protocol):
    """Protocol for backend graph builders.

    后端图构建器的协议定义。
    """

    def build(
        self,
        reviews: Sequence[dict],
        metadata: Dict[str, dict],
        entity_maps: Dict[str, Dict[str, int]],
        edge_schema: Sequence[EdgeType],
    ) -> object:
        """Build and return a backend-specific graph object.

        构建并返回后端特定的图对象。
        """
