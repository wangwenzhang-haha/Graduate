"""Entity encoding utilities.

实体编码工具函数。
"""

from __future__ import annotations

from typing import Iterable


def _encode_values(values: Iterable[str]) -> dict[str, int]:
    """Encode unique string values into integer IDs.

    将唯一字符串值编码为整数 ID。
    """
    mapping: dict[str, int] = {}
    for value in values:
        # Skip empty values. / 跳过空值。
        if not value:
            continue
        if value not in mapping:
            mapping[value] = len(mapping)
    return mapping


def encode_entities(
    reviews: list[dict],
    metadata: dict[str, dict],
    use_brand: bool = True,
    use_category: bool = True,
) -> dict[str, dict[str, int]]:
    """Encode entity identifiers for heterogeneous graph construction.

    为异构图构建编码实体标识。
    """
    # Collect unique users and items from reviews. / 从评论中收集用户与物品。
    users = [str(row.get("user")) for row in reviews if row.get("user")]
    items = [str(row.get("item")) for row in reviews if row.get("item")]

    # Ensure items from metadata are included. / 确保包含元数据中的物品。
    items.extend([str(item_id) for item_id in metadata.keys() if item_id])

    entity_maps: dict[str, dict[str, int]] = {
        # Encode users and items first. / 先编码用户与物品。
        "user": _encode_values(users),
        "item": _encode_values(items),
    }

    if use_brand:
        # Collect brand names when enabled. / 启用时收集品牌名称。
        brands = [
            str(info.get("brand"))
            for info in metadata.values()
            if isinstance(info, dict) and info.get("brand")
        ]
        entity_maps["brand"] = _encode_values(brands)

    if use_category:
        # Collect category labels when enabled. / 启用时收集类别标签。
        categories: list[str] = []
        for info in metadata.values():
            if not isinstance(info, dict):
                continue
            category_list = info.get("categories", [])
            if isinstance(category_list, list):
                categories.extend(str(cat) for cat in category_list if cat)
        entity_maps["category"] = _encode_values(categories)

    return entity_maps
