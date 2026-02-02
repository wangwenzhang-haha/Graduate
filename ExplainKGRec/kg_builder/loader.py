"""Load raw review/meta datasets."""

from __future__ import annotations

import gzip
import json
from typing import Iterator


def parse_json_gz(path: str) -> Iterator[dict]:
    """Stream JSON objects from a gzip-compressed JSONL file.

    从 gzip 压缩的 JSONL 文件中按行读取 JSON 对象。
    """
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def load_amazon_reviews(path: str) -> list[dict]:
    """Load Amazon review data into a normalized schema.

    将 Amazon 评论数据归一化为统一结构。
    """
    records: list[dict] = []
    for row in parse_json_gz(path):
        # Skip rows without required identifiers. / 跳过缺少必要标识的记录。
        user = row.get("reviewerID")
        item = row.get("asin")
        if not user or not item:
            continue
        records.append(
            {
                # Normalize to string identifiers. / 标准化为字符串标识。
                "user": str(user),
                "item": str(item),
                # Review text may be missing. / 评论文本可能缺失。
                "text": str(row.get("reviewText", "")) if row.get("reviewText") else "",
                # Rating may be missing; keep None. / 评分可能缺失，保留 None。
                "rating": float(row["overall"]) if row.get("overall") is not None else None,
            }
        )
    return records


def load_amazon_metadata(path: str) -> dict[str, dict]:
    """Load Amazon metadata into a normalized schema keyed by ASIN.

    按 ASIN 键组织 Amazon 元数据并归一化字段。
    """
    metadata: dict[str, dict] = {}
    for row in parse_json_gz(path):
        # Ignore rows without ASIN. / 忽略缺少 ASIN 的记录。
        asin = row.get("asin")
        if not asin:
            continue
        # Description may be list or string. / 描述可能为列表或字符串。
        description = row.get("description")
        if isinstance(description, list):
            description = description[0] if description else ""
        # Categories are nested paths; take first path. / 类目为多级路径，取第一条路径。
        categories = row.get("categories")
        categories_list: list[str] = []
        if isinstance(categories, list) and categories:
            first_path = categories[0]
            if isinstance(first_path, list):
                categories_list = [str(cat) for cat in first_path]
        metadata[str(asin)] = {
            # Title text. / 标题文本。
            "title": str(row.get("title", "")) if row.get("title") else "",
            # Description text. / 描述文本。
            "description": str(description) if description else "",
            # Brand name. / 品牌名称。
            "brand": str(row.get("brand", "")) if row.get("brand") else "",
            # Flattened categories. / 扁平化类目路径。
            "categories": categories_list,
        }
    return metadata


def load_yelp_reviews(path: str) -> list[dict]:
    """Placeholder for Yelp review loading.

    Yelp 评论加载的占位函数。
    """
    raise NotImplementedError("Yelp review loading is not implemented yet.")


def load_wikidata_triples(path: str) -> list[tuple[str, str, str]]:
    """Placeholder for Wikidata triple loading.

    Wikidata 三元组加载的占位函数。
    """
    raise NotImplementedError("Wikidata triple loading is not implemented yet.")
