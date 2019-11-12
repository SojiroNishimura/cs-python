from typing import NamedTuple, List


class Item(NamedTuple):
    name: str
    weight: int
    value: float


def knapsack(items: List[Item], max_capacity: int) -> List[Item]:
    # 動的計画法のテーブルを作成
    table: List[List[float]] = [[0.0 for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]
    for i, item in enumerate(items):
        for capacity in range(1, max_capacity + 1):
            previous_items_value: float = table[i][capacity]
            if capacity >= item.weight: # 品物がナップサックに入る場合
                value_freeing_weight_for_item: float = table[i][capacity - item.weight]
                # 以前より価値が高くなるなら入れる
                table[i + 1][capacity] = max(value_freeing_weight_for_item + item.value, previous_items_value)
            else: # 容量不足
                table[i + 1][capacity] = previous_items_value
    
    # テーブルから解を得る
    solution: List[Item] = []
    capacity = max_capacity
    for i in range(len(items), 0, -1): # 後ろ向きに作業
        # 品物を入れたか？
        if table[i - 1][capacity] != table[i][capacity]:
            solution.append(items[i - 1])
            # 品物を入れたら容量を減らす
            capacity -= items[i - 1].weight
    return solution


if __name__ == "__main__":
    items: List[Item] = [Item("television", 50, 500),
        Item("candlesticks", 2, 300),
        Item("stereo", 35, 400),
        Item("laptop", 3, 1000),
        Item("food", 15, 50),
        Item("clothing", 20, 800),
        Item("jewelry", 1, 4000),
        Item("books", 100, 300),
        Item("printer", 18, 30),
        Item("refrigerator", 200, 700),
        Item("painting", 10, 1000)]
    print(knapsack(items, 75))