# ExplainKGRec: 结构增强的推荐解释系统

**ExplainKGRec** 是在 [XRec](https://github.com/HKUDS/XRec) 基础上扩展的推荐解释系统，旨在引入异构知识图谱与结构路径控制能力，提升推荐系统的可解释性与结构可控性。

---

## 🔍 项目动机

尽管 XRec 构建了基于用户/商品简介与 LLM 的推荐解释框架，但其交互图较为稀疏，且推荐理由生成主要依赖语言模型自由生成，缺乏结构控制能力。本项目通过：

* 引入 **异质知识图谱**（用户-物品-类别-品牌-常识概念）
* 构建 **显式多跳解释路径（ExplainPath）**
* 利用大模型生成 **结构驱动的推荐理由**

实现解释的个性化、结构化、可追溯。

---

## 🧱 模块结构

```
ExplainKGRec/
├── kg_builder/         # 知识图谱构建模块（替代 XRec 的 process/）
│   ├── loader.py         # 通用数据加载（支持 Amazon/Wikidata 等）
│   ├── encoder.py        # 实体 ID 编码器（user/item/brand/category/...）
│   ├── graph_builder/     # 图构建模块主目录（后端无关）
│   │   ├── __init__.py    # 注册统一接口，如 build_graph_backend(backend='dgl')
│   │   ├── base.py        # 通用图构建接口规范与数据结构定义
│   │   ├── builder_dgl.py # 用 DGL 构建异构图
│   │   ├── builder_pyg.py # 用 PyG 构建异构图（可选）
│   │   └── builder_nx.py  # 用 NetworkX 构建图（如只需路径提取时）
│   ├── text_embedder.py  # 使用 BERT 提取 item 文本特征
│   ├── external_kg.py    # 加载外部结构化知识（如 Wikidata）
│   ├── merge_graphs.py   # 多源图谱融合逻辑
│   └── utils.py          # 辅助工具函数
│
├── explanation/        # 推荐路径提取与解释构造模块
│   ├── structure_extract.py  # 从图中提取用户相关的解释路径
│   ├── path_score.py        # 路径过滤与排序规则
│   ├── path_to_text.py      # 路径转自然语言解释（模板驱动）
│   ├── rag_prompt.py        # 构造用于 LLM 的提示词输入
│   └── types.py             # ExplainPath 数据结构定义
│
├── explainer/          # 微调与调用大语言模型（沿用 XRec 结构）
├── encoder/            # 图神经网络模型（支持 LightGCN / R-GCN / HGT）
├── generation/         # 生成用户/商品简介模块（可选）
├── evaluation/         # 自动评估模块（文本+结构指标）
└── data/               # 各类数据集和图谱结果
```

---

## ✅ 项目主要特性

* 支持多源异构图谱融合（用户行为、商品元数据、文本抽取、外部知识）
* 构建显式结构路径，服务推荐解释
* 与大语言模型融合，通过 Prompt 注入结构控制信号
* 可插拔图神经网络编码器
* 保留 XRec 的用户简介、商品简介微调能力

---

## 📦 数据支持

* 支持处理 Amazon、Yelp、Google Play 等说明型推荐数据
* 可挂接 ConceptNet / Wikidata 等开放图谱
* 图结构可序列化保存为 `.bin` 或 `.pt`

---

## 🚧 开发进度

* [x] 完成 kg_builder/loader.py
* [ ] 实现 kg_builder/encoder.py
* [ ] 完善异构图构建 pipeline
* [ ] 接入结构路径提取逻辑
* [ ] 联动 LLM + Prompt 构造

---

## 📄 致谢

本项目参考并基于以下优秀项目构建：

* [XRec (HKU)](https://github.com/HKUDS/XRec)
* [DGL](https://github.com/dmlc/dgl)
* [ConceptNet](https://github.com/commonsense/conceptnet5)
* [OpenAI API](https://platform.openai.com/docs)
