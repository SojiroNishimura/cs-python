from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod


T = TypeVar('T', bound='Chromosome')


# 全染色体の基底クラス。全メソッドがオーバーライドされる
class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float:
        ...

    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...

    @abstractmethod
    def crossover(self, other: T) -> Tuple[T, T]:
        ...

    @abstractmethod
    def mutate(self) -> None:
        ...