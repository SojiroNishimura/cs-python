from __future__ import annotations
from dataclasses import dataclass
from edge import Edge


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.v, self.u, self.weight)

    # 辺を重み順にして最小重み辺を求める
    def __lt__(self, other: WeightedEdge):
        return self.weight < other.weight

    def __str__(self) -> str:
        return f"{self.u} {self.weight}> {self.v}"