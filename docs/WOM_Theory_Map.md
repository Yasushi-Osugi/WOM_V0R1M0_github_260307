#WOM_Theory_Map.md
WOM Theory Map
                       WOM THEORY MAP
                (Unified Economic Planning Theory)



                    ┌──────────────────────────┐
                    │     Nation Objective     │
                    │ Wellbeing / Stability    │
                    │ Growth / Sustainability  │
                    └─────────────┬────────────┘
                                  │
                                  │ Evaluation
                                  │
                          ┌───────▼────────┐
                          │ Evaluation     │
                          │ Function U(S)  │
                          └───────┬────────┘
                                  │
                                  │ Optimization
                                  │
                         ┌────────▼─────────┐
                         │     Resolver      │
                         │   Decision Search │
                         │                   │
                         │ Beam / MCTS / RL  │
                         └────────┬─────────┘
                                  │
                                  │ Operator
                                  │
                         ┌────────▼─────────┐
                         │   Planning Space  │
                         │                   │
                         │ State Space       │
                         │ Action Space      │
                         │ Evaluation Space  │
                         └────────┬─────────┘
                                  │
                                  │ State
                                  │
                         ┌────────▼─────────┐
                         │ Planning Tensor   │
                         │                   │
                         │ S = (D,F,I,C)     │
                         │                   │
                         │ Demand Tensor     │
                         │ Flow Tensor       │
                         │ Inventory Tensor  │
                         │ Capacity Tensor   │
                         └────────┬─────────┘
                                  │
                                  │ Dynamics
                                  │
                         ┌────────▼─────────┐
                         │  Flow Network     │
                         │                   │
                         │ Factory           │
                         │ Warehouse         │
                         │ Market            │
                         └────────┬─────────┘
                                  │
                                  │ Physical Flow
                                  │
                         ┌────────▼─────────┐
                         │ Economic Field    │
                         │                   │
                         │ Price Field       │
                         │ Cost Field        │
                         │ Demand Pressure   │
                         └────────┬─────────┘
                                  │
                                  │ Demand Signal
                                  │
                         ┌────────▼─────────┐
                         │        CPU        │
                         │ Household Demand  │
                         └───────────────────┘
WOM Theory Map の意味

この図は 6層構造です。

1 CPU（需要の源）
Household
Market
Region

需要の発生源です。

2 Economic Field

価格・コスト・需要が
経済場 (economic field) を作ります。

3 Flow Network

供給チェーンです。

Factory
Warehouse
Market
4 Planning Tensor

状態

S = (D,F,I,C)
5 Planning Space

すべての計画状態の集合

State
Action
Evaluation
6 Resolver Search

意思決定探索

Beam Search
Monte Carlo
RL
Rule based
7 Evaluation

評価関数

Profit
Service
Inventory
Risk
8 Nation Objective

最終目的

Wellbeing
Stability
Productivity
Sustainability
WOM理論の最終式

WOM Theory Mapは
次の式を説明しています。

S^{*} = \arg\max_{A_{0:T}} U(T(S_0,A_{0:T}))

意味

最適計画
=
最適なオペレーター列

です。

WOM Theory Map の本質

この理論は

Economics
Supply Chain
Optimization
AI

を統合します。

非常に重要

この Theory Map を見ると
WOM は

Supply Chain Tool

ではなく

Economic Planning Engine

です。

そして実は

この Theory Map をさらに整理すると
WOMの理論は たった6つの概念に集約されます。

CPU
Price
Lot
Flow
Resolver
Evaluation

これをまとめたものが

WOM Core Theory

です。
