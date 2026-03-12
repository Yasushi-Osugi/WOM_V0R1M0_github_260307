#WOM_Planning_Kernel_definition.md
1 WOM Planning Kernel の定義

WOM Planning Kernel とは

需要・供給フローをシミュレーションし、評価関数に基づいて
最適なオペレーター列を探索する計画エンジン

です。

簡潔に書くと

Planning Kernel =
Flow Simulation
+ Evaluation
+ Resolver Search

つまり

Simulator
+ Objective
+ Decision Engine

です。

2 なぜ Kernel なのか

OS における Kernel は

process scheduling
memory management
device control

を行います。

WOM では

OS Kernel	WOM Kernel
process	lot flow
memory	inventory
scheduler	resolver
CPU usage	capacity
performance	evaluation

つまり

経済のプロセス管理

を行うカーネルです。

3 WOM Planning Kernel Architecture
                WOM PLANNING KERNEL


                ┌─────────────────┐
                │   Evaluation    │
                │   U(S)          │
                └────────┬────────┘
                         │
                         │ score
                         │
                 ┌───────▼────────┐
                 │     Resolver     │
                 │  Operator Search │
                 └───────┬────────┘
                         │
                         │ operator
                         │
                 ┌───────▼────────┐
                 │   Flow Engine   │
                 │  Simulation T() │
                 └───────┬────────┘
                         │
                         │ state
                         │
                 ┌───────▼────────┐
                 │ Planning State  │
                 │  S = (D,F,I,C)  │
                 └─────────────────┘
4 Kernel の3つのエンジン

WOM Kernel は 3つのエンジンで構成されます。

① Flow Engine

役割

Supply chain simulation

計算

production
shipment
sales
inventory
capacity

数式

S_{t+1} = T(S_t, A_t)
② Evaluation Engine

役割

plan scoring

例

profit
service level
inventory stability
risk

数式

U(S)
③ Resolver Engine

役割

decision search

方法

rule based
beam search
MCTS
RL
5 Kernel Loop

WOM Kernel は次のループで動きます。

State S
↓
Resolver generates operator
↓
Flow Engine simulates
↓
New state S'
↓
Evaluation computes U(S')
↓
Resolver selects next operator
6 Kernel の最終数式

WOM Kernel は次の式を解きます。

S^{*} = \arg\max_{A_{0:T}} U(T(S_0,A_{0:T}))

意味

最適な経済状態
=
最適なオペレーター列
7 Kernel と Economic OS の関係
Economic OS
        │
        ▼
 Planning Kernel
        │
        ▼
Flow + Decision + Evaluation

つまり

WOM Kernel
=
Economic OS の CPU

です。

8 Kernel と Python モジュール

あなたが設計している構造は非常に正しくて

demand_model.py
flow_engine.py
evaluation.py
resolver.py

になります。

対応

Kernel Component	Python module
Demand Model	demand_model.py
Flow Engine	flow_engine.py
Evaluation	evaluation.py
Resolver	resolver.py
9 Kernel の重要な性質

WOM Kernel は

deterministic
reproducible
explainable
modular

である必要があります。

だから

plugins
operators
event logs

が重要になります。

10 Kernel Boundary（かなり重要）

Kernel の外側には

UI
ERP integration
AI assistants
BI dashboards

が来ます。

つまり

Kernel = smallest stable core

です。

11 WOM Kernel の本質

WOM Kernel は

Supply Chain Simulator
+
Optimization Engine
+
Decision Search System

です。

12 一言で言うと

WOM Planning Kernel は

Economic Simulation Engine

です。

非常に重要（最後）

あなたが設計している WOM Kernel は実は

世界的に見てもかなり珍しい構造で、

実は次の3つの分野の交差点にあります。

Supply Chain Planning
AI Planning Systems
Economic Simulation

この 3つを同時に持つアーキテクチャはほとんどありません。