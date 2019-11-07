from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome


C = TypeVar('C', bound=Chromosome) # 染色体の型


class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT")

    def __init__(self, initial_population: List[C], threshold: float, max_generations: int = 100,
        mutation_chance: float = 0.01, crossover_chance: float = 0.7, selection_type = SelectionType.TOURNAMENT) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

    # 確率分布のルーレットで2つの親を選ぶ(負の適応度ではうまくおかない)
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights=wheel, k=2))

    # num個の無作為抽出した個体から最良の2つを選ぶ
    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    # 母集団を新世代の個体で入れ替え
    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        while len(new_population) < len(self._population):
            # 両親を選ぶ
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents: Tuple[C, C] = self._pick_roulette([x.fitness() for x in self._population])
            else:
                parents = self._pick_tournament(len(self._population) // 2)
            # 両親の交差の可能性
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        # 奇数個なら1つ取り除く
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population

    # 個体は_mutation_chanceの確率で変異
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    # max_generations世代の遺伝的アルゴリズムを実行し最良個体を返す
    def run(self) -> C:
        best: C = max(self._population, key=self._fitness_key)

        for generation in range(self._max_generations):
            if best.fitness() >= self._threshold: # early exit if we beat threshold
                return best
            print(f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest # 新たな最良個体発見
        return best