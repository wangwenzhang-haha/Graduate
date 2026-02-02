"""Schema registry for graph construction.

图构建结构注册中心。
"""

from __future__ import annotations

# Node type list for heterogeneous graphs. / 异构图节点类型列表。
NODE_TYPES: list[str] = ["user", "item", "brand", "category"]

# Optional node type aliases for compact notation. / 节点类型的可选别名映射。
NODE_TYPE_ALIAS: dict[str, str] = {
    "user": "U",
    "item": "I",
    "brand": "B",
    "category": "C",
}

# Canonical edge types for the KG schema. / 知识图谱的标准边类型定义。
EDGE_TYPES: list[tuple[str, str, str]] = [
    ("user", "buys", "item"),
    ("item", "produced_by", "brand"),
    ("item", "belongs_to", "category"),
]

# Reverse edge mapping for directional relations. / 方向边的逆向关系映射。
REVERSE_EDGE_MAP: dict[tuple[str, str, str], tuple[str, str, str]] = {
    ("user", "buys", "item"): ("item", "bought_by", "user"),
    ("item", "produced_by", "brand"): ("brand", "produces", "item"),
    ("item", "belongs_to", "category"): ("category", "includes", "item"),
}

# Edge types relevant to explanation tasks. / 解释任务相关的边类型。
EXPLANATION_RELEVANT_EDGES: list[str] = ["buys", "belongs_to"]

# Edge types used for message passing. / 图传播使用的边类型。
PROPAGATION_EDGES: list[str] = ["buys", "produced_by"]

# Valid path templates for explanation paths. / 解释路径的合法模板。
VALID_PATH_TEMPLATES: list[list[str]] = [
    ["user", "buys", "item", "belongs_to", "category"],
    ["user", "buys", "item", "produced_by", "brand"],
]
