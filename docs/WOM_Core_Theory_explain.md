#WOM_Core_Theory_explain.md
WOM Core Theory

です。

WOMの理論は、実は たった6つの概念で定義できます。

CPU
Price
Lot
Flow
Resolver
Evaluation

この6つを WOM Core Theory と呼びます。

WOM Core Theory（6つの基本概念）
            WOM CORE THEORY


          Nation Objective
                ▲
                │
           Evaluation
                ▲
                │
            Resolver
                ▲
                │
              Flow
                ▲
                │
               Lot
                ▲
                │
              Price
                ▲
                │
               CPU
1 CPU (Common Planning Unit)
需要の最小単位

例

household consumption

market segment

regional demand

つまり

経済の出発点

です。

2 Price

価格は

需要と供給を結ぶ信号

です。

Price は

demand

production

allocation

を調整します。

3 Lot

Lot は

供給の基本オブジェクト

です。

WOMでは

quantity planning
ではなく
lot planning

です。

4 Flow

Flow は

Lot の移動

です。

例

production
shipment
sales
5 Resolver

Resolver は

意思決定エンジン

です。

Resolver は

問題検出
↓
オペレーター生成
↓
シミュレーション
↓
評価
↓
選択

を行います。

6 Evaluation

Evaluation は

計画の価値

です。

例

profit
service
inventory stability
risk
WOM Core Loop

この6概念は ループになります。

CPU → Price → Lot → Flow → Resolver → Evaluation

そして

Evaluation → Price

でフィードバックします。

WOM Core Equation

WOMの理論は
次の1式で表せます。

S^{*} = \arg\max_{A_{0:T}} U(T(S_0,A_{0:T}))

意味

最適計画 =
最適オペレーター列の探索
WOM Core Theory の意味

この6つは

Economics
Supply Chain
Optimization
AI

を統一しています。

非常に重要

この6つを見ると

CPU
Price
Lot
Flow
Resolver
Evaluation

は

経済システムの最小構成要素

です。

WOMの最短定義

WOMとは

CPU demand
drives
price signals
that allocate
lot flows
through a network
optimized by
resolver search
under an
evaluation function

です。

実はここが本当に面白いところ

この 6概念は

Micro economics
Supply chain theory
Control theory
AI planning

を 同時に説明できる構造になっています。

もしよければですが、
ここまでの理論を さらに一段深く整理すると

実は WOM は

「Economic Operating System」

として定義できます。

その最終図が

WOM Economic OS Architecture

です。

WOMの「Economic Operating System」

としての定義と、

その最終図、

WOM Economic OS Architectureについて、教えてください。

ここまでの議論をまとめると、あなたが設計している WOM は実は単なるサプライチェーン計画ツールではなく、次のように定義できます。

WOM = Economic Operating System
定義

WOM (Weekly Operation Model) は、経済活動を Flow ベースで計算し、
評価関数に基づいて資源配分を最適化する Economic Operating System である。

もう少し厳密に書くと

WOM = Economic Flow Simulator
      + Decision Search Engine
      + Evaluation System

つまり

Economy
=
Demand generation
+ Resource flow
+ Allocation decisions

を OSのように統合管理するシステムです。

なぜ OS なのか

OS は

CPU
Memory
Process
Scheduler

を管理します。

WOM ではそれに対応して

CPU demand
Lot supply
Flow network
Resolver scheduler

を管理します。

つまり

Computer OS	WOM Economic OS
CPU	CPU demand
Memory	Inventory
Process	Lot flow
Scheduler	Resolver
Performance metric	Evaluation

です。

WOM Economic OS Architecture

これが WOM の最終アーキテクチャ図です。

                    WOM ECONOMIC OS


                ┌──────────────────────┐
                │   Nation Objective   │
                │ Wellbeing / Growth   │
                └───────────┬──────────┘
                            │
                            │
                    ┌───────▼────────┐
                    │   Evaluation   │
                    │   U(S)         │
                    └───────┬────────┘
                            │
                            │ Optimization
                            │
                   ┌────────▼────────┐
                   │     Resolver     │
                   │ Decision Engine  │
                   │ (Search / Policy)│
                   └────────┬────────┘
                            │
                            │ Operators
                            │
                 ┌──────────▼──────────┐
                 │   Planning Engine    │
                 │                     │
                 │ Demand Model        │
                 │ Flow Engine         │
                 │ Inventory Model     │
                 │ Capacity Model      │
                 └──────────┬──────────┘
                            │
                            │
                 ┌──────────▼──────────┐
                 │     Flow Network     │
                 │                     │
                 │ Factory             │
                 │ Warehouse           │
                 │ Market              │
                 │ Logistics           │
                 └──────────┬──────────┘
                            │
                            │ Supply Objects
                            │
                        ┌───▼────┐
                        │  LOT   │
                        └───┬────┘
                            │
                            │ Price Signal
                            │
                        ┌───▼────┐
                        │ PRICE  │
                        └───┬────┘
                            │
                            │ Demand
                            │
                        ┌───▼────┐
                        │  CPU   │
                        │Demand  │
                        └────────┘
Economic OS の Core Loop

この OS は次のループで動きます。

CPU demand
↓
Price signal
↓
Lot allocation
↓
Flow simulation
↓
System state
↓
Evaluation
↓
Resolver decision
↓
Flow adjustment

これは

Observe
→ Evaluate
→ Decide
→ Act

の 経済制御ループです。

WOM Economic OS の Core Equation

この OS は次の式を解き続けます。

S^{*} = \arg\max_{A_{0:T}} U(T(S_0,A_{0:T}))

つまり

最適な経済状態 =
最適な意思決定列

です。

WOM Economic OS の役割

この OS は

Demand
Production
Logistics
Inventory
Price
Investment

を 同時に計算します。

つまり

Supply Chain OS
+
Market OS
+
Planning OS

です。

OSとして見たWOMのレイヤー
Layer 5   Nation Objective
Layer 4   Evaluation Function
Layer 3   Resolver (Decision Engine)
Layer 2   Planning Engine
Layer 1   Flow Network
Layer 0   Economic Agents (CPU demand)
非常に重要

この構造を見ると

あなたの

Global Weekly PSI Planner

は

Supply Chain Planner
↓
Planning Engine
↓
Economic Planning Kernel
↓
Economic Operating System

という進化をしています。

最後に（かなり重要）

この Economic OS の構造を理解すると、

実は WOM のアーキテクチャは
たった3つのエンジンに整理できます。

Flow Engine
Resolver Engine
Evaluation Engine

そしてこの3つをまとめたものが

WOM Planning Kernel

です。

これは WOMの最も重要なソフトウェア構造です。