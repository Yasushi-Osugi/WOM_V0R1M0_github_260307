#WOM_Planning_Kernel_explain.md
WOM Planning Kernel の本質は「複雑なコード」ではなく、実はとても小さいループです。
その最小構造を示すと、約200行程度の Python で Kernel の骨格が書けます。

ポイントは次の4モジュールだけです。

demand_model
flow_engine
evaluation
resolver

これを 1つの Kernel Loopで回します。

1 WOM Kernel の最小構造

Kernel は次のループです。

initialize state
↓
generate demand
↓
simulate flows
↓
evaluate state
↓
resolver decides operator
↓
apply operator
↓
repeat

これだけです。

2 最小データ構造

まず状態 S を定義します。

from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    demand: np.ndarray
    inventory: np.ndarray
    flow: np.ndarray
    capacity: np.ndarray

これは

S = (D, F, I, C)

の実装です。

3 Demand Model

CPU と Price から需要を生成します。

class DemandModel:

    def generate(self, cpu, price):
        base = cpu * 10
        elasticity = -0.5
        demand = base * (price ** elasticity)
        return demand

数式

D = f(CPU, Price)
4 Flow Engine

Flow Engine は supply chain をシミュレーションします。

class FlowEngine:

    def simulate(self, state):

        production = np.minimum(
            state.capacity,
            state.demand
        )

        shipment = production

        new_inventory = (
            state.inventory
            + production
            - shipment
        )

        state.inventory = new_inventory
        state.flow = shipment

        return state

これは

I(t+1) = I(t) + inflow − outflow

です。

5 Evaluation

評価関数

class Evaluation:

    def score(self, state):

        service = np.minimum(
            state.flow,
            state.demand
        ).sum()

        inventory_penalty = state.inventory.sum()

        score = service - 0.1 * inventory_penalty

        return score

これは

U(S)

です。

6 Resolver

Resolver は operator を決めます。

class Resolver:

    def propose(self, state):

        if state.inventory.mean() < 10:
            return {"type": "increase_capacity"}

        if state.inventory.mean() > 50:
            return {"type": "reduce_production"}

        return {"type": "do_nothing"}
7 Operator Application
def apply_operator(state, operator):

    if operator["type"] == "increase_capacity":
        state.capacity *= 1.1

    if operator["type"] == "reduce_production":
        state.capacity *= 0.9

    return state
8 Kernel Loop

ここが WOM Kernel の核心です。

class PlanningKernel:

    def __init__(self):

        self.demand_model = DemandModel()
        self.flow_engine = FlowEngine()
        self.evaluation = Evaluation()
        self.resolver = Resolver()

    def run(self, state, cpu, price, steps=20):

        history = []

        for t in range(steps):

            # demand
            state.demand = self.demand_model.generate(cpu, price)

            # simulate
            state = self.flow_engine.simulate(state)

            # evaluate
            score = self.evaluation.score(state)

            # resolver
            operator = self.resolver.propose(state)

            # apply operator
            state = apply_operator(state, operator)

            history.append((t, score, operator))

        return history
9 実行例
state = State(
    demand=np.zeros(5),
    inventory=np.ones(5)*20,
    flow=np.zeros(5),
    capacity=np.ones(5)*15
)

kernel = PlanningKernel()

history = kernel.run(
    state,
    cpu=100,
    price=1.0,
    steps=30
)

print(history)
10 これが WOM Kernel

このコードは

Flow Simulation
Evaluation
Resolver

を回しています。

つまり

S(t)
↓
T(S)
↓
U(S)
↓
Resolver

です。

11 数式との対応
数学	Python
S	State
T(S)	FlowEngine
U(S)	Evaluation
A	Operator
Resolver	Resolver
12 Kernel の本質

このコードは

200 lines

程度ですが、

理論的には

Economic Planning Engine

です。

非常に重要

ここまで見ると分かると思いますが、

あなたが作っている

Global Weekly PSI Planner

は実は

Supply Chain Tool
↓
Planning Engine
↓
Economic Simulation Kernel

です。