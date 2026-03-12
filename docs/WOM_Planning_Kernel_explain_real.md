#WOM_Planning_Kernel_explain_real.md
さきほどの200行 Kernel は、かなり抽象化した

demand

inventory

flow

capacity

の最小ループでした。

これを WOM の実際の PSI モデル（LOT_IDベース） に近づけると、次の変化が起きます。

1. 何が変わるのか

最小 Kernel では、状態はこうでした。

State(
    demand=np.ndarray,
    inventory=np.ndarray,
    flow=np.ndarray,
    capacity=np.ndarray,
)

これは 数量ベースです。

WOM の PSI モデルでは、これが

数量
→
LOT_ID を持つ event / flow の集合

に変わります。

つまり、中心が

配列

から

LOT付きイベント列

に変わります。

2. WOM PSI モデルの最小構成

LOT_IDベースにすると、最小の実体はこの5つです。

Lot
FlowEvent
Node
StateView
Operator

特に重要なのはこの2つです。

Lot

供給の識別子

FlowEvent

その Lot がどこで何をしたかの記録

つまり、

Lot = 物の identity
Event = 物の movement / transformation

です。

3. LOT_IDベースのデータ構造

最小形はこうなります。

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass(frozen=True)
class Lot:
    lot_id: str
    product_id: str
    qty: float
    origin_node: str
    due_week: str

@dataclass(frozen=True)
class FlowEvent:
    event_id: str
    lot_id: str
    event_type: str   # production, shipment, arrival, sale
    from_node: Optional[str]
    to_node: Optional[str]
    week: str
    qty: float

ここで重要なのは、在庫を主テーブルにしないことです。

在庫は

arrival の累積
-
shipment / sale の累積

から計算します。

4. State の作り方が変わる

最小 Kernel では inventory を state に直接持っていましたが、
WOM では state は event から派生します。

たとえば

@dataclass
class StateView:
    inventory_by_node_product_week: dict
    backlog_by_node_product_week: dict
    capacity_usage_by_node_week: dict

これを作る関数はこうです。

def derive_state(events: List[FlowEvent]) -> StateView:
    inventory = {}
    backlog = {}
    capacity = {}

    for ev in events:
        key = (ev.to_node or ev.from_node, ev.week)

        if ev.event_type == "production":
            capacity[key] = capacity.get(key, 0) + ev.qty

        if ev.event_type == "arrival":
            inv_key = (ev.to_node, ev.week)
            inventory[inv_key] = inventory.get(inv_key, 0) + ev.qty

        if ev.event_type in ("shipment", "sale"):
            inv_key = (ev.from_node, ev.week)
            inventory[inv_key] = inventory.get(inv_key, 0) - ev.qty

    return StateView(
        inventory_by_node_product_week=inventory,
        backlog_by_node_product_week=backlog,
        capacity_usage_by_node_week=capacity,
    )

かなり単純ですが、思想はもう WOM です。

5. Demand も LOT と結びつく

WOMらしくするには、Demand も単なる数量でなく、
どの市場・どの週・どの商品に対する要求かを持たせます。

@dataclass(frozen=True)
class DemandEvent:
    demand_id: str
    market_node: str
    product_id: str
    week: str
    qty: float

そして Resolver は

どの Lot を
どの Demand に
どの週で割り当てるか

を考えます。

ここで初めて PSIらしい供給割当 になります。

6. Flow Engine の役割

LOT_IDベースの Flow Engine は、配列計算ではなく

event list を生成・変換するエンジン

になります。

最小の役割は次です。

demand に対して lot を割り当てる

production event を作る

shipment event を作る

arrival event を作る

sale event を作る

その結果から state を作る

概念コードはこうです。

class FlowEngine:

    def simulate(
        self,
        lots: list[Lot],
        demand_events: list[DemandEvent],
        capacities: dict
    ) -> list[FlowEvent]:

        events = []

        for lot in lots:
            # 生産
            events.append(
                FlowEvent(
                    event_id=f"prod_{lot.lot_id}",
                    lot_id=lot.lot_id,
                    event_type="production",
                    from_node=None,
                    to_node=lot.origin_node,
                    week=lot.due_week,
                    qty=lot.qty,
                )
            )

            # 仮の shipment / arrival / sale
            events.append(
                FlowEvent(
                    event_id=f"ship_{lot.lot_id}",
                    lot_id=lot.lot_id,
                    event_type="shipment",
                    from_node=lot.origin_node,
                    to_node="MARKET",
                    week=lot.due_week,
                    qty=lot.qty,
                )
            )

            events.append(
                FlowEvent(
                    event_id=f"arr_{lot.lot_id}",
                    lot_id=lot.lot_id,
                    event_type="arrival",
                    from_node=lot.origin_node,
                    to_node="MARKET",
                    week=lot.due_week,
                    qty=lot.qty,
                )
            )

            events.append(
                FlowEvent(
                    event_id=f"sale_{lot.lot_id}",
                    lot_id=lot.lot_id,
                    event_type="sale",
                    from_node="MARKET",
                    to_node=None,
                    week=lot.due_week,
                    qty=lot.qty,
                )
            )

        return events

実際の WOM ではここに

lead time

node capacity

route

priority

inventory carry-over

が乗ります。

7. Resolver が LOT を直接扱う

ここが一番重要です。

最小 Kernel では Resolver は capacity を上下させるだけでした。
WOM PSI モデルでは Resolver は Lot の運命を変えます。

たとえば operator はこうなります。

@dataclass(frozen=True)
class Operator:
    operator_type: str
    lot_id: str
    params: dict

例:

shift_production_week

shift_shipment_week

reroute_lot

split_lot

allocate_to_priority_market

つまり Resolver は

state を直接変えるのでなく
Lot/Event を編集する

のです。

これが WOM の核心です。

8. LOT_IDベースの Kernel Loop

すると全体ループはこうなります。

class PlanningKernel:

    def __init__(self):
        self.flow_engine = FlowEngine()
        self.evaluator = Evaluator()
        self.resolver = Resolver()

    def run(self, lots, demand_events, capacities, max_iter=10):
        current_lots = lots
        history = []

        for step in range(max_iter):
            events = self.flow_engine.simulate(current_lots, demand_events, capacities)
            state = derive_state(events)
            score = self.evaluator.score(state)

            trust_events = detect_trust_events(state, capacities)
            if not trust_events:
                history.append((step, score, "stable"))
                break

            op = self.resolver.propose(trust_events, current_lots, events, state)
            current_lots = apply_operator_to_lots(current_lots, op)

            history.append((step, score, op))

        return current_lots, history

これで構造としてはもう

LOT_IDベースの WOM Kernel です。

9. どこが PSI なのか

WOM の PSI は、従来のような

P / S / I の表

を直接更新するのではありません。

WOM では

production events の集計が P

sale / shipment events の集計が S

events の累積差分が I

です。

つまり

PSI = event stream の view

です。

これがかなり大きい違いです。

10. LOT_IDベースにすると何が嬉しいか

利点はかなり大きいです。

1. explainable

「なぜこの在庫になったか」を Lot 単位で追える

2. operatorが自然

shift / reroute / split が Lot に対して定義できる

3. monthly / weekly 整合が良い

weekly event を月次集計すれば monthly PSI になる

4. trust_events と相性が良い

どの Lot が overflow や stockout の原因か追える

11. 逆に難しくなる点

もちろん難しさもあります。

1. event 数が増える

配列より管理対象が増える

2. lot split が難しい

1つの Lot を分割するルールが必要

3. event ordering が重要

週・優先度・生成順を deterministic にしないと壊れる

4. state を直接触りたくなる誘惑

でも触ると WOM の kernel が壊れる

12. 一言でいうと

200行の最小 Kernel を WOM PSI モデルにすると、

配列ベースの計画器
↓
LOT_ID付き event-driven planning kernel

になります。

つまり、

State-first
↓
Event-first

への変換です。

13. 実際のあなたのコードに近い見方

あなたの実コードに寄せて言えば、
WOM の LOT_IDベース Kernel は次の形です。

Node が network 上の拠点

Lot が supply object

PSI が lot/event の累積 view

Resolver が operator を探す

Evaluation が plan を採点する

つまり

Node network
+ Lot objects
+ Event stream
+ State derivation
+ Operator search

です。

これはかなり明確に WOMらしい骨格です。

14. 最後に重要なこと

この構造にすると、WOM は

Supply Chain Planning Tool

ではなく

Lot-based Economic Planning Kernel

になります。

ここまで来ると、次に本当に重要なのは
**「LOT_IDベースの最小クラス設計」**です。

つまり

Lot

FlowEvent

DemandEvent

StateView

Operator

PlanningKernel

の6クラスを、WOM向けに最小でどう定義するかです。