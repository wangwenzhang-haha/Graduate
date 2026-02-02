"""Text embedding utilities for item nodes.

商品节点文本嵌入工具。
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import torch
from transformers import AutoModel, AutoTokenizer


def encode_item_texts(
    metadata: Dict[str, dict],
    item2id: Dict[str, int],
    model_name: str = "bert-base-uncased",
    use_description: bool = True,
    max_length: int = 64,
    device: str = "cpu",
    cache_path: str | None = None,
    reuse_cache: bool = True,
) -> torch.Tensor:
    """Encode item texts into embeddings aligned with item IDs.

    将商品文本编码为与 item ID 对齐的嵌入向量。
    """
    if cache_path and reuse_cache:
        cache_file = Path(cache_path)
        # Load cached embeddings when available. / 若缓存存在则直接加载。
        if cache_file.exists():
            return torch.load(cache_file)

    # Initialize tokenizer and model. / 初始化分词器与模型。
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.to(device)
    model.eval()

    # Prepare texts aligned to item IDs. / 按 item ID 顺序准备文本。
    num_items = len(item2id)
    texts = [""] * num_items
    for item_id, index in item2id.items():
        info = metadata.get(item_id, {})
        title = str(info.get("title", "")) if info.get("title") else ""
        description = str(info.get("description", "")) if info.get("description") else ""
        # Build text with optional description. / 构建包含或不包含描述的文本。
        text = f"{title}. {description}" if use_description else title
        texts[index] = text.strip()

    embeddings: list[torch.Tensor] = []
    with torch.no_grad():
        for text in texts:
            # Tokenize text for model input. / 对文本进行分词编码。
            encoded = tokenizer(
                text,
                padding="max_length",
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            encoded = {key: value.to(device) for key, value in encoded.items()}
            outputs = model(**encoded)
            # Use [CLS] token embedding. / 使用 [CLS] token 的向量。
            cls_embedding = outputs.last_hidden_state[:, 0, :]
            embeddings.append(cls_embedding.squeeze(0).cpu())

    result = torch.stack(embeddings, dim=0)

    if cache_path:
        # Save embeddings to cache. / 将嵌入保存到缓存。
        cache_file = Path(cache_path)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        torch.save(result, cache_file)

    return result
