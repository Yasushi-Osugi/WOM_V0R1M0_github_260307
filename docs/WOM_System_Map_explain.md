#WOM_System_Map_explain.md
WOM System Map（Final）
                          WOM SYSTEM MAP
                    (Economic Planning Engine)


                         NATION OBJECTIVE
              ─────────────────────────────────
              Wellbeing / Stability / Growth
              Productivity / Sustainability


                                ▲
                                │
                                │ Evaluation Function
                                │
                         ┌──────┴──────┐
                         │   RESOLVER  │
                         │─────────────│
                         │ Search      │
                         │ Operators   │
                         │ Policy      │
                         └──────┬──────┘
                                │
                                │ Action
                                │
                     ┌──────────┴──────────┐
                     │   PLANNING SPACE    │
                     │─────────────────────│
                     │ State Space         │
                     │ Action Space        │
                     │ Evaluation Space    │
                     └──────────┬──────────┘
                                │
                                │ State
                                │
                     ┌──────────┴──────────┐
                     │   ECONOMIC FIELD     │
                     │──────────────────────│
                     │ Price Field          │
                     │ Cost Field           │
                     │ Demand Field         │
                     │ Profit Potential     │
                     └──────────┬───────────┘
                                │
                                │ Gradient
                                │
                     ┌──────────┴──────────┐
                     │  ECONOMIC TENSOR     │
                     │──────────────────────│
                     │ Demand Tensor        │
                     │ Flow Tensor          │
                     │ Inventory Tensor     │
                     │ Capacity Tensor      │
                     └──────────┬───────────┘
                                │
                                │ Flow Dynamics
                                │
                     ┌──────────┴──────────┐
                     │     FLOW NETWORK     │
                     │──────────────────────│
                     │ Factory              │
                     │ Warehouse            │
                     │ Market               │
                     │ Logistics            │
                     └──────────┬───────────┘
                                │
                                │ Supply Object
                                │
                         ┌──────┴──────┐
                         │     LOT     │
                         │─────────────│
                         │ Production  │
                         │ Shipment    │
                         │ Allocation  │
                         └──────┬──────┘
                                │
                                │ Demand
                                │
                         ┌──────┴──────┐
                         │    PRICE    │
                         │ Market Signal│
                         └──────┬──────┘
                                │
                                │ Consumption
                                │
                         ┌──────┴──────┐
                         │      CPU     │
                         │ Household    │
                         │ Demand Unit  │
                         └──────────────┘
この図の意味

この System Map は 経済を8層で表現しています。

1 CPU（最下層）
CPU = Common Planning Unit

家庭の消費です。

例

食料

電力

自動車

住宅

つまり

経済の需要の源泉

2 Price

価格は

需要と供給を結ぶ信号

です。

価格は

demand

production

flow

を調整します。

3 Lot

Lotは

供給の基本オブジェクト

です。

WOMでは

quantity planning
ではなく
lot planning

です。

4 Flow Network

ここが Supply Chain Physics です。

Factory → Warehouse → Market

Flowは

production
shipment
sales

の動きです。

5 Economic Tensor

経済状態は

CPU × Product × Location × Time

のテンソルになります。

つまり

Demand Tensor
Flow Tensor
Inventory Tensor
Capacity Tensor

です。

6 Economic Field

ここで

Price
Cost
Demand
Profit

が **経済場（economic field）**を作ります。

この場の勾配が

Economic Gravity

です。

7 Planning Space

ここで

State
Action
Evaluation

の 探索空間ができます。

Resolverは

この空間を探索

します。

8 Resolver

Resolverは

planning search engine

です。

役割

Detect
Generate Operator
Simulate
Evaluate
Select
9 Nation Objective（最上位）

最終目標です。

例

Wellbeing
Stability
Productivity
Knowledge
WOM System Map の本質

この図を一言で言うと

Household demand
↓
Supply chain physics
↓
Economic tensor
↓
Economic field
↓
Planning space
↓
Resolver search
↓
Nation objective

です。

WOM の本当の正体

この図で見ると WOM は

Supply Chain Planner

ではなく

Economic Simulation Engine

でもなく

Economic Operating System

です。

非常に重要

この System Map を見ると

あなたのプロジェクトは

Global Weekly PSI Planner
↓
WOM Planning Kernel
↓
Economic Planning Engine
↓
Economic OS

という構造です。
