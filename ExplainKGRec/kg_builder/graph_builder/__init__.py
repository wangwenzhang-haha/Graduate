"""Graph builder backend registry.

图构建后端注册入口。
"""

from __future__ import annotations

from typing import Literal

from .builder_dgl import build_graph_dgl


def build_graph_backend(backend: Literal["dgl"]) -> callable:
    """Return graph builder callable for the selected backend.

    返回指定后端的图构建函数。
    """
    if backend == "dgl":
        return build_graph_dgl
    raise ValueError(f"Unsupported backend: {backend}")
