from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    u: int # from 節点
    v: int # to 節点

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"